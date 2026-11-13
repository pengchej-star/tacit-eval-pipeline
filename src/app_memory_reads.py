"""Which parts of memory/ an agent opened, read from its Claude Code stream-json transcript, and a check of the
report's knowledge_used against that.

Used by app_iterate.py after every memory run (written to meta.json as memory_reads and knowledge_used_unopened).
Also works on finished runs, including Yaqing's (transcript.jsonl from run_application.py):

  python src/app_memory_reads.py RUN_DIR [RUN_DIR ...]          # print the summary
  python src/app_memory_reads.py --write RUN_DIR [RUN_DIR ...]  # also add it to RUN_DIR/meta.json

File names map to tree nodes: memory/attention/t-7-3-<slug>.md is node T.7.3, memory/cases/t-7-3-4-<slug>.md is
option T.7.3.4, t-<slug>.md without numbers is the root T. Check codes (E129) are taken from searches and from reads
of evidence/registry.md.
"""

import json
import re
import sys
from pathlib import Path

PATH_RE = re.compile(r"(?<![\w-])(memory/[A-Za-z0-9_.*/-]*)")
ECODE_RE = re.compile(r"\bE\d{2,3}\b")
SEGMENT_RE = re.compile(r";|&&|\|\||(?<=\s)\|(?=\s)|\n")   # a pipe needs spaces around it, so grep 'E1\|E2' stays whole
LIST_CMDS = {"ls", "find", "tree", "du", "wc"}
SEARCH_CMDS = {"grep", "egrep", "rg", "ag"}


def node_of(path: str):
    name = Path(path).name
    m = re.match(r"t-((?:\d+-)*\d+)-", name)
    if m:
        return "T." + m.group(1).replace("-", ".")
    return "T" if name.startswith("t-") else None


def _part(path: str):
    p = path.split("/")
    return p[1] if len(p) > 2 else (p[1] if len(p) == 2 and p[1] else "")


HEREDOC_RE = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?[^\n]*\n(.*?)\n\s*\1\b", re.S)
OPEN_RE = re.compile(r"open\(\s*['\"]([^'\"]*memory/[^'\"]+)['\"]")


def _bash_events(cmd: str):
    """Heredoc bodies are mostly text the agent writes (code, report.json citing memory files), so only open('memory/...')
    inside them counts as a read; the rest of the command is split into simple commands."""
    out = []
    for m in HEREDOC_RE.finditer(cmd):
        out += [{"kind": "read", "path": p} for p in PATH_RE.findall(" ".join(OPEN_RE.findall(m.group(2))))]
    cmd = HEREDOC_RE.sub(lambda m: m.group(0).split("\n", 1)[0], cmd)
    for seg in SEGMENT_RE.split(cmd):
        words = seg.strip().split()
        while words and ("=" in words[0] or words[0] in ("sudo", "command", "xargs")):
            words = words[1:]
        first = Path(words[0]).name if words else ""
        kind = "list" if first in LIST_CMDS else "search" if first in SEARCH_CMDS else "read"
        partial = first in ("head", "tail", "sed", "awk")
        for p in PATH_RE.findall(seg):
            k = "list" if ("*" in p or p.endswith("/") or "." not in Path(p).name) and kind == "read" else kind
            ev = {"kind": k, "path": p.rstrip("/")}
            if k == "read" and partial:
                ev["partial"] = True
            if k == "search":
                ev["codes"] = sorted(set(ECODE_RE.findall(seg)))
            out.append(ev)
    return out


def memory_reads(transcript: Path) -> dict:
    """Ordered memory events and a summary of what was opened."""
    events, step = [], 0
    for line in Path(transcript).read_text(errors="replace").splitlines():
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if msg.get("type") != "assistant":
            continue
        for c in msg.get("message", {}).get("content", []) or []:
            if not isinstance(c, dict) or c.get("type") != "tool_use":
                continue
            step += 1
            name, inp = c.get("name"), c.get("input") or {}
            found = []
            if name == "Read":
                for p in PATH_RE.findall(inp.get("file_path", "")):
                    ev = {"kind": "read", "path": p}
                    if inp.get("offset") or inp.get("limit"):
                        ev["partial"] = True
                    found.append(ev)
            elif name == "Grep":
                for p in PATH_RE.findall(inp.get("path", "") + " " + inp.get("glob", "")):
                    found.append({"kind": "search", "path": p.rstrip("/"), "codes": sorted(set(ECODE_RE.findall(inp.get("pattern", ""))))})
            elif name == "Glob":
                for p in PATH_RE.findall(inp.get("pattern", "") + " " + inp.get("path", "")):
                    found.append({"kind": "list", "path": p.rstrip("/")})
            elif name == "Bash":
                found = _bash_events(inp.get("command", ""))
            for ev in found:
                events.append({"step": step, "tool": name, **ev})

    reads = [e for e in events if e["kind"] == "read"]
    files = list(dict.fromkeys(e["path"] for e in reads))
    codes = set()
    for e in events:
        codes.update(e.get("codes", []))
    return {
        "events": events,
        "files_read": files,
        "taxonomy_read": any(f.endswith("taxonomy.md") for f in files),
        "nodes_read": list(dict.fromkeys(n for f in files if _part(f) == "attention" and (n := node_of(f)))),
        "cases_read": list(dict.fromkeys(n for f in files if _part(f) == "cases" and (n := node_of(f)))),
        "registry_read": any(f.endswith("evidence/registry.md") for f in files),
        "evidence_codes_searched": sorted(codes),
        "n_tool_calls": step,
    }


TREE_ID_RE = re.compile(r"\bT(?:\.\d+)*\b")


def check_knowledge_used(report: dict, reads: dict) -> list:
    """knowledge_used items that the transcript does not back: the decision's attention file was never opened, or
    cases are cited but the option's cases file was never opened."""
    nodes, cases = set(reads["nodes_read"]), set(reads["cases_read"])
    issues = []
    for i, k in enumerate(report.get("knowledge_used") or []):
        if not isinstance(k, dict):
            issues.append({"item": i, "issue": "not an object"})
            continue
        node = (TREE_ID_RE.findall(str(k.get("node") or "")) or [None])[0]
        option = (TREE_ID_RE.findall(str(k.get("option") or "")) or [None])[0]
        if node and node not in nodes:
            issues.append({"item": i, "node": node, "issue": "attention file of this decision not opened"})
        if k.get("cases") and option not in cases:
            issues.append({"item": i, "option": option, "issue": "cases cited but this option's cases file not opened"})
    return issues


def main(argv):
    write = "--write" in argv
    for d in [Path(a) for a in argv if a != "--write"]:
        reads = memory_reads(d / "transcript.jsonl")
        report = {}
        if (d / "report.json").exists():
            try:
                report = json.loads((d / "report.json").read_text())
            except json.JSONDecodeError:
                pass
        issues = check_knowledge_used(report, reads)
        print(f"== {d}")
        print(json.dumps({k: v for k, v in reads.items() if k != "events"}, indent=1))
        for e in reads["events"]:
            print(f"  step {e['step']:>3} {e['tool']:<5} {e['kind']:<6} {e['path']}{' (partial)' if e.get('partial') else ''}"
                  f"{' codes ' + ','.join(e['codes']) if e.get('codes') else ''}")
        print("knowledge_used:", len(report.get("knowledge_used") or []), "items; unopened:", issues or "none")
        if write and (d / "meta.json").exists():
            meta = json.loads((d / "meta.json").read_text())
            meta.update(memory_reads=reads, knowledge_used_unopened=issues)
            (d / "meta.json").write_text(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main(sys.argv[1:])
