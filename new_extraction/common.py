"""LLM client (CMU LiteLLM proxy, Azure fallback), embeddings, tolerant JSON parsing, resumable thread-pool helper, config."""
import hashlib, json, os, re, sys, time
from pathlib import Path

import numpy as np
import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
CFG = yaml.safe_load(open(ROOT / "config.yaml", encoding="utf-8"))
# run.py can override the mode / expert count / output suffix through the environment (read before any other module is imported)
if os.environ.get("NE_MODE"):
    CFG["items"]["mode"] = os.environ["NE_MODE"]
if os.environ.get("NE_NEXPERTS"):
    CFG["scope"]["n_experts"] = int(os.environ["NE_NEXPERTS"])
TASKS = yaml.safe_load(open(ROOT / "tasks.yaml", encoding="utf-8"))     # per competition: name, direction (max|min), description
COMPS = [c.strip() for c in os.environ["NE_COMPS"].split(",")] if os.environ.get("NE_COMPS") else list(CFG["scope"]["comps"] or TASKS)
MODE = CFG["items"]["mode"]
assert MODE in ("episode", "label"), MODE
OUT = ROOT / CFG["paths"]["out"] / ("pooled_" + MODE + os.environ.get("NE_SUFFIX", ""))   # all competitions together
OUT.mkdir(exist_ok=True, parents=True)
API_BASE = CFG["litellm"]["api_base"]
PREFIX = CFG["litellm"]["prefix"]


def fill(template, **slots):
    """Replace <<name>> in a prompt template by config `task:` values and by keyword slots (slots win)."""
    vals = {**{k: str(v).strip() for k, v in CFG["task"].items()}, **{k: str(v) for k, v in slots.items()}}
    out = re.sub(r"<<(\w+)>>", lambda m: vals[m.group(1)] if m.group(1) in vals else m.group(0), template)
    left = re.findall(r"<<(\w+)>>", out)
    assert not left, f"unfilled prompt slots: {left}"
    return out


def stage_model(stage):
    """Model for a stage: config stage_models[stage], else model.generator."""
    return (CFG.get("stage_models") or {}).get(stage, CFG["model"]["generator"])


def api_key():
    k = os.environ.get("LITELLM_API_KEY", "").strip()
    if not k:
        raise RuntimeError("LITELLM_API_KEY is empty (copy .env.example to .env and fill it in)")
    return k


def azure_deployments():
    out = {}
    for k, v in os.environ.items():
        n = re.fullmatch(r"AZURE_OPENAI_MODEL_NAME_(\d+)", k)
        if n:
            ep, key = (os.environ.get(f"AZURE_OPENAI_{x}_{n.group(1)}", "").strip() for x in ("ENDPOINT", "API_KEY"))
            if ep and key:
                out[v.strip()] = (ep, key)
    return out


def call_azure(model, msgs, max_tokens, temperature, timeout):
    import requests
    name = model.removeprefix(PREFIX).removeprefix("wine-")
    dep = azure_deployments()
    if name not in dep:
        raise RuntimeError(f"no Azure deployment for {name}")
    ep, key = dep[name]
    body = dict(model=name, max_tokens=max_tokens, temperature=temperature, messages=[x for x in msgs if x["role"] != "system"],
                system="\n\n".join(x["content"] for x in msgs if x["role"] == "system"))
    r = requests.post(ep, json=body, timeout=timeout, headers={"x-api-key": key, "api-key": key, "anthropic-version": "2023-06-01"})
    if r.status_code != 200:
        raise RuntimeError(f"Azure {name}: HTTP {r.status_code} {r.text[:300]}")
    return "".join(b.get("text", "") for b in r.json()["content"] if b.get("type") == "text")


def call_model(system, user, model=None, max_tokens=None, temperature=None):
    """One chat completion -> text. Retries the proxy, then the same model on Azure."""
    import litellm
    litellm.suppress_debug_info = True
    m = CFG["model"]
    msgs = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    model = model or m["generator"]
    mt = max_tokens or m["max_tokens"]
    temp = m["temperature"] if temperature is None else temperature
    errs = []
    for a in range(m["max_retries"]):
        try:
            q = model if model.startswith(PREFIX) else PREFIX + model
            r = litellm.completion(api_key=api_key(), base_url=API_BASE, model=q, messages=msgs, max_tokens=mt,
                                   temperature=temp, timeout=m["timeout_s"])
            return r.choices[0].message.content
        except Exception as e:
            errs.append(f"proxy: {e}")
            time.sleep(2 ** a)
    for a in range(m["max_retries"]):
        try:
            return call_azure(model, msgs, mt, temp, m["timeout_s"])
        except Exception as e:
            errs.append(f"azure: {e}")
            time.sleep(2 ** a)
    raise RuntimeError(" | ".join(errs)[-600:])


def parse_json(txt):
    txt = re.sub(r"^```(?:json)?|```$", "", (txt or "").strip(), flags=re.M).strip()
    try:
        return json.loads(txt)
    except Exception:
        for pat in (r"\{.*\}", r"\[.*\]"):
            m = re.search(pat, txt, flags=re.S)
            if m:
                try:
                    return json.loads(m.group(0))
                except Exception:
                    pass
    return {"_raw": txt}


def ask(system, user, **kw):
    """call_model + parse_json; one retry if the reply is not JSON."""
    for _ in range(2):
        r = parse_json(call_model(system, user, **kw))
        if not (isinstance(r, dict) and "_raw" in r):
            return r
    return r


def pmap(fn, items, workers=None, desc=""):
    """Order-preserving thread-pool map with progress."""
    import concurrent.futures as cf
    workers = workers or CFG["model"]["workers"]
    out = [None] * len(items)
    t0 = time.time()
    with cf.ThreadPoolExecutor(workers) as ex:
        futs = {ex.submit(fn, it): i for i, it in enumerate(items)}
        for n, f in enumerate(cf.as_completed(futs), 1):
            try:
                out[futs[f]] = f.result()
            except Exception as e:
                out[futs[f]] = {"_error": str(e)[:300]}
            if n % 25 == 0 or n == len(items):
                print(f"  [{desc}] {n}/{len(items)} ({time.time() - t0:.0f}s)", flush=True)
    return out


def cached_jsonl(path, items, fn, key, workers=None, desc=""):
    """Run fn(item)->dict for items whose key is not yet in `path`; each result is appended to the file as soon as it is done, so an
    interrupted run loses at most the calls in flight. Returns {key: record}. Failed calls are reported and not stored."""
    import concurrent.futures as cf
    path = Path(path)
    done = {}
    if path.exists():
        for l in open(path, encoding="utf-8"):
            r = json.loads(l)
            done[r["_key"]] = r
    todo = [it for it in items if key(it) not in done]
    print(f"{desc}: {len(done)} cached, {len(todo)} to run", flush=True)
    if todo:
        t0 = time.time()
        with cf.ThreadPoolExecutor(workers or CFG["model"]["workers"]) as ex, open(path, "a", encoding="utf-8") as f:
            futs = {ex.submit(fn, it): it for it in todo}
            for n, fu in enumerate(cf.as_completed(futs), 1):
                it = futs[fu]
                try:
                    r = fu.result()
                    if r is None or "_error" in r:
                        raise RuntimeError((r or {}).get("_error"))
                except Exception as e:
                    print(f"  [{desc}] FAILED {key(it)}: {str(e)[:200]}", flush=True)
                    continue
                r = {**r, "_key": key(it)}
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
                f.flush()
                done[key(it)] = r
                if n % 25 == 0 or n == len(todo):
                    print(f"  [{desc}] {n}/{len(todo)} ({time.time() - t0:.0f}s)", flush=True)
    return done


def cached_batches(path, items, fn, key, batch_size, workers=None, desc=""):
    """Like cached_jsonl, but one LLM call handles `batch_size` items: fn(list of items) -> list of dicts aligned with the list (None = no
    answer). Records are cached per item (same file layout as cached_jsonl), so batch size can change between runs. Items a batch call
    left unanswered are retried alone. Returns {key: record}."""
    import concurrent.futures as cf
    path = Path(path)
    done = {}
    if path.exists():
        for l in open(path, encoding="utf-8"):
            r = json.loads(l)
            done[r["_key"]] = r
    todo = [it for it in items if key(it) not in done]
    chunks = [todo[i:i + batch_size] for i in range(0, len(todo), batch_size)]
    print(f"{desc}: {len(done)} cached, {len(todo)} to run in {len(chunks)} calls", flush=True)

    def one_chunk(chunk):
        res = fn(chunk) if len(chunk) > 1 else [None]
        res = list(res) if isinstance(res, list) and len(res) == len(chunk) else [None] * len(chunk)
        for i, r in enumerate(res):
            if not isinstance(r, dict) or "_error" in r:
                single = fn([chunk[i]])
                res[i] = single[0] if isinstance(single, list) and single else None
        return res

    if chunks:
        t0 = time.time()
        with cf.ThreadPoolExecutor(workers or CFG["model"]["workers"]) as ex, open(path, "a", encoding="utf-8") as f:
            futs = {ex.submit(one_chunk, c): c for c in chunks}
            for n, fu in enumerate(cf.as_completed(futs), 1):
                chunk = futs[fu]
                try:
                    res = fu.result()
                except Exception as e:
                    print(f"  [{desc}] FAILED a batch of {len(chunk)}: {str(e)[:200]}", flush=True)
                    continue
                for it, r in zip(chunk, res):
                    if not isinstance(r, dict):
                        print(f"  [{desc}] no answer for {key(it)}", flush=True)
                        continue
                    r = {**r, "_key": key(it)}
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
                    done[key(it)] = r
                f.flush()
                if n % 25 == 0 or n == len(chunks):
                    print(f"  [{desc}] {n}/{len(chunks)} calls ({time.time() - t0:.0f}s)", flush=True)
    return done


def embed(texts):
    """L2-normalised embeddings, cached on disk by sha1(model+text)."""
    from openai import OpenAI
    E = CFG["embedding"]
    cp = ROOT / CFG["paths"]["out"] / "embed_cache.json"   # shared by all competitions
    cache = json.loads(cp.read_text()) if cp.exists() else {}
    key = lambda t: hashlib.sha1((E["model"] + "\n" + t).encode()).hexdigest()
    todo = sorted({t for t in texts if key(t) not in cache})
    if todo:
        cl = OpenAI(api_key=api_key(), base_url=API_BASE.rstrip("/") + "/v1")
        for i in range(0, len(todo), E["batch"]):
            b = todo[i:i + E["batch"]]
            r = cl.embeddings.create(model=E["model"], input=b)
            for t, d in zip(b, sorted(r.data, key=lambda d: d.index)):
                cache[key(t)] = d.embedding
        cp.write_text(json.dumps(cache))
    X = np.array([cache[key(t)] for t in texts], dtype=np.float64)
    return X / np.linalg.norm(X, axis=1, keepdims=True)


def jdump(obj, path):
    Path(path).write_text(json.dumps(obj, indent=1, ensure_ascii=False, default=str), encoding="utf-8")


def jload(path):
    return json.load(open(path, encoding="utf-8"))


def index(t, d=None):
    d = d if d is not None else {}
    d[t["id"]] = t
    for c in t.get("children") or []:
        index(c, d)
    return d
