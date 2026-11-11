"""Build a self-contained side-by-side HTML viewer: bottom-up tree (2b) vs merged tree (3).
Usage: python3 tools/make_tree_compare.py [out_dir] [out_html]"""
import json, sys, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
d = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else root / "out/pooled_episode"
out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else root / "tree_compare.html"

items = {i["id"]: {"ctx": (i.get("instance") or {}).get("context") or i.get("why", ""),
                   "act": (i.get("instance") or {}).get("action") or i.get("what", ""),
                   "comp": i.get("comp", ""), "expert": i.get("expert", "")}
         for i in json.load(open(d / "2a_items.json"))}


# step-4 desiderata: 4_desiderata.jsonl is keyed by node id + name (4_desiderata.json only exists after the dedupe step)
desid = {}
if (d / "4_desiderata.jsonl").exists():
    for l in open(d / "4_desiderata.jsonl", encoding="utf-8"):
        r = json.loads(l)
        desid[r["_key"]] = r.get("groups", [])


def bu(n):
    kids = [bu(c) for c in n.get("children", [])]
    return {"id": n["id"], "name": n["label"], "sub": n.get("question") or "",
            "text": n.get("summary") or "", "level": n["level"], "option": n.get("option"),
            "ne": len(n.get("experts", [])), "experts": n.get("experts", []), "items": n.get("items", []), "children": kids}


def mg(n):
    chk = n.get("check") or {}
    names = {c["id"]: c["name"] for c in n.get("children", [])}
    groups = [{"under": g.get("under", ""),
               "checks": [{"check": c.get("check", ""), "how": c.get("how", ""),
                           "pushes": [[names.get(k, k), v] for k, v in (c.get("pushes") or {}).items()]}
                          for c in g.get("checks", [])]}
              for g in desid.get(n["id"] + n["name"], [])]
    return {"id": n["id"], "name": n["name"], "sub": n.get("decision") or "",
            "text": n.get("description") or "", "level": n.get("depth"), "source": n.get("source"),
            "ne": len(n.get("experts", [])), "experts": n.get("experts", []), "ni": n.get("n_edits", len(n.get("all_items", []))),
            "items": n.get("items", []), "actions": n.get("actions", []),
            "desid": groups, "empty": n.get("n_edits", 0) == 0,
            "issues": [f'{i["child"]}: {i["problem"]}' for i in chk.get("issues", [])],
            "children": [mg(c) for c in n.get("children", [])]}


b = json.load(open(d / "2b_bottomup.json"))
m = json.load(open(d / "3_merged_tree.json"))
data = {"bu": bu(b["root"]), "mg": mg(m), "items": items}
html = TEMPLATE = open(root / "tools/tree_compare_template.html").read()
out.write_text(html.replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")))
print("wrote", out, f"{out.stat().st_size/1e6:.1f} MB")
