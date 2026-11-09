"""LLM access via the CMU LiteLLM proxy, falling back to the same Claude model on Azure AI Foundry when the proxy fails.

    from llm import call_model, parse_json
    obj = parse_json(call_model(system, user, model="wine-claude-opus-4-6", temperature=0, max_tokens=6000))

Keys come from .env (LITELLM_API_KEY, optional AZURE_OPENAI_{ENDPOINT,API_KEY,MODEL_NAME}_<n>); see .env.example.
Smoke test: python llm.py
"""
import json, os, re, sys, time
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
load_dotenv(ROOT.parent / ".env")  # a shared .env one level up is also read; values already set are not overridden
CFG = yaml.safe_load(open(ROOT / "config.yaml", encoding="utf-8"))
API_BASE = CFG["litellm"]["api_base"]
PREFIX = CFG["litellm"].get("prefix", "openai/")


def api_key():
    k = os.environ.get("LITELLM_API_KEY", "").strip()
    if not k:
        raise RuntimeError("LITELLM_API_KEY is empty. Put your key in .env (see .env.example).")
    return k


def qualify(model):
    """'wine-claude-opus-4-6' -> 'openai/wine-claude-opus-4-6' (the proxy speaks the OpenAI protocol)."""
    return model if model.startswith(PREFIX) else PREFIX + model


def azure_deployments():
    """{model name: (endpoint, key)} from the numbered AZURE_OPENAI_* variables."""
    out = {}
    for k, v in os.environ.items():
        n = re.fullmatch(r"AZURE_OPENAI_MODEL_NAME_(\d+)", k)
        ep, key = (os.environ.get(f"AZURE_OPENAI_{x}_{n.group(1)}", "").strip() for x in ("ENDPOINT", "API_KEY")) if n else ("", "")
        if ep and key:
            out[v.strip()] = (ep, key)
    return out


def call_azure(model, msgs, max_tokens, temperature, timeout):
    """One Anthropic Messages API call on Azure AI Foundry; 'wine-claude-opus-4-6' -> deployment 'claude-opus-4-6'."""
    import requests
    name = model.removeprefix(PREFIX).removeprefix("wine-")
    if name not in azure_deployments():
        raise RuntimeError(f"no Azure deployment for {name} in .env (have: {', '.join(azure_deployments()) or 'none'})")
    ep, key = azure_deployments()[name]
    body = dict(model=name, max_tokens=max_tokens, temperature=temperature, messages=[x for x in msgs if x["role"] != "system"])
    system = "\n\n".join(x["content"] for x in msgs if x["role"] == "system")
    if system:
        body["system"] = system
    r = requests.post(ep, json=body, timeout=timeout, headers={"x-api-key": key, "api-key": key, "anthropic-version": "2023-06-01"})
    if r.status_code != 200:
        raise RuntimeError(f"Azure {name}: HTTP {r.status_code} {r.text[:300]}")
    return "".join(b.get("text", "") for b in r.json()["content"] if b.get("type") == "text")


_fell_back = False


def call_model(system, user, model=None, max_tokens=None, temperature=None, **kw):
    """One chat completion; returns the assistant text. Retries the proxy, then the same model on Azure."""
    import litellm
    litellm.suppress_debug_info = True
    global _fell_back
    m = CFG["model"]
    msgs = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    model = model or m["generator"]
    max_tokens = max_tokens if max_tokens is not None else m["max_tokens"]
    temperature = temperature if temperature is not None else m["temperature"]
    errors = []
    for attempt in range(m.get("max_retries", 3)):
        try:
            r = litellm.completion(api_key=api_key(), base_url=API_BASE, model=qualify(model), messages=msgs,
                                   max_tokens=max_tokens, temperature=temperature, timeout=m.get("timeout_s", 120), **kw)
            return r.choices[0].message.content
        except Exception as e:  # rate limit / timeout / 5xx: back off and retry
            errors.append(f"proxy: {e}")
            if "LITELLM_API_KEY is empty" in str(e) or "AuthenticationError" in type(e).__name__ or "tokens per day" in str(e):
                break  # retrying cannot help; go to Azure
            time.sleep(2 ** attempt)
    if not _fell_back:
        _fell_back = True
        print(f"[llm] proxy failed for {model} ({errors[-1][:150]}); falling back to Azure", file=sys.stderr, flush=True)
    for attempt in range(m.get("max_retries", 3)):
        try:
            return call_azure(model, msgs, max_tokens, temperature, m.get("timeout_s", 120))
        except Exception as e:
            errors.append(f"azure: {e}")
            if "no Azure deployment" in str(e):
                break
            time.sleep(2 ** attempt)
    raise RuntimeError(" | ".join(errors))


def parse_json(txt):
    """Tolerant JSON parse of a model reply (strips fences, falls back to the first {...} block)."""
    txt = re.sub(r"^```(?:json)?|```$", "", (txt or "").strip(), flags=re.M).strip()
    try:
        return json.loads(txt)
    except Exception:
        m = re.search(r"\{.*\}", txt, flags=re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
    return {"_raw": txt}


def pmap_jsonl(items, fn, path, key=lambda r: r["step_id"], workers=8, desc=""):
    """Run fn(item) -> dict in a thread pool, appending each result as one JSON line to `path`.
    Items whose key is already in the file are skipped, so an interrupted run can be resumed. Returns all records in item order."""
    import concurrent.futures as cf
    path = Path(path)
    done = {}
    if path.exists():
        for l in open(path, encoding="utf-8"):
            r = json.loads(l); done[key(r)] = r
    todo = [it for it in items if key(it) not in done]
    print(f"{desc}: {len(done)} done, {len(todo)} to run, {workers} workers", flush=True)
    with cf.ThreadPoolExecutor(workers) as ex, open(path, "a", encoding="utf-8") as f:
        for rec in ex.map(fn, todo):
            f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
            done[key(rec)] = rec
    return [done[key(it)] for it in items if key(it) in done]


if __name__ == "__main__":
    t0 = time.time()
    print(f"[{CFG['model']['generator']}, {time.time() - t0:.1f}s]",
          call_model("You are a helpful assistant.", "Reply with the single word: pong", max_tokens=50, temperature=0))
