"""Add the agents' trees (runs/<agent>/output) to ../tree_compare.html and make the displayed trees selectable.
Run again after a new agent run to refresh the data. Usage: python build_compare.py"""
import json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
HTML = HERE.parent / "tree_compare.html"
AGENTS = [("claude", "Claude Code (sonnet 5.5)"), ("codex", "Codex (gpt-6-astra)")]

s = HTML.read_text()
i, j = s.index("const D="), s.index("\nconst esc=")
D = json.loads(s[i + 8:j].rstrip().rstrip(";"))
D.pop("ag", None)

def convert(n, des, items, depth=0):
    """agent node -> the node shape of the merged tree ('mg') so build() renders it unchanged"""
    kids = [convert(c, des, items, depth + 1) for c in n.get("children") or []]
    its = list(n.get("items") or []) if not kids else []
    allit = its + [x for k in kids for x in k["all_items"]]
    experts = sorted({items[x]["expert"] for x in allit if x in items})
    names = {c["id"]: c["name"] for c in n.get("children") or []}
    desid = [dict(under=g["under"], checks=[dict(check=c["check"], how=c.get("how", ""),
              pushes=[[names.get(k, k), v] for k, v in (c.get("pushes") or {}).items()]) for c in g["checks"]])
             for g in (des.get(n["id"]) or {}).get("groups", [])]
    return dict(id=n["id"], name=n["name"], sub=n.get("decision", ""), text=n.get("description", ""), level=depth,
                source={"data": "bottom_up", "prior": "top_down"}.get(n.get("source"), "both"),
                ne=len(experts), experts=experts, ni=len(allit), all_items=allit, items=its, actions=[], desid=desid,
                empty=not allit, issues=[], children=kids)

ag = {}
for key, title in AGENTS:
    out = HERE / "runs" / key / "output"
    if not (out / "tree.json").exists():
        print("skip", key, "(no output)"); continue
    t = json.load(open(out / "tree.json")); des = json.load(open(out / "desiderata.json"))["nodes"]
    root = convert(t, des, D["items"])
    if t.get("unassigned"):
        un = [u["item"] for u in t["unassigned"]]
        root["children"].append(dict(id="unassigned", name="Unassigned", sub="", text="; ".join(u["reason"] for u in t["unassigned"][:5]),
            level=1, source="both", ne=0, experts=[], ni=len(un), all_items=un, items=un, actions=[], desid=[], empty=False, issues=[], children=[]))
    ag[key] = dict(title=title, root=root)
D["ag"] = ag

def strip(n):
    n.pop("all_items", None)
    for c in n["children"]: strip(c)
for a in ag.values(): strip(a["root"])

if "/*multi*/" not in s:
    # one-time patch of the page: panes are created from a list of trees, chosen with checkboxes
    s = re.sub(r'<div id="wrap">.*?</div>\n<script>', '<div id="wrap"></div>\n<script>', s, count=1, flags=re.S)
    s = s.replace('<div id="bar">\n', '<div id="bar">\n <span id="sel">Trees: </span>\n', 1)
    s = s.replace("<title>Tree compare: bottom-up vs merged</title>", "<title>Tree compare</title>", 1)
    old = "mount('L',D.bu,'bu');mount('R',D.mg,'mg');"
    assert old in s
    s = s.replace(old, """/*multi*/
const TREES=[{key:'bu',title:'Bottom-up (2b_bottomup.json) — root at top level, leaves = actions',kind:'bu',root:D.bu,on:false},
 {key:'mg',title:'Merged tree (3_merged_tree.json) — skeleton + observed',kind:'mg',root:D.mg,on:false}]
 .concat(Object.entries(D.ag||{}).map(([k,a])=>({key:k,title:a.title+' — agent_tree/runs/'+k,kind:'mg',root:a.root,on:true})));
function show(t){
 const w=document.getElementById('wrap'),p=document.createElement('div');p.className='pane';p.id='pane_'+t.key;
 p.innerHTML=`<div class="head"><span class="t">${esc(t.title)}</span></div><div class="body" id="B_${t.key}"></div>`;
 const before=TREES.slice(TREES.indexOf(t)+1).map(x=>document.getElementById('pane_'+x.key)).find(Boolean);
 w.insertBefore(p,before||null);mount('B_'+t.key,t.root,t.kind);
}
function hide(t){const p=document.getElementById('pane_'+t.key);if(p)p.remove();delete roots['B_'+t.key]}
TREES.forEach(t=>{
 const l=document.createElement('label');l.style.marginRight='8px';
 l.innerHTML=`<input type="checkbox" ${t.on?'checked':''}> ${esc(t.key)}`;
 l.firstChild.onchange=e=>{e.target.checked?show(t):hide(t);const q=document.getElementById('q').value.trim().toLowerCase();if(q.length>=2)search(q)};
 document.getElementById('sel').appendChild(l);
 if(t.on)show(t);
});""", 1)
    s = s.replace(".pane{flex:1 1 50%;width:50%;", ".pane{flex:1 1 0;", 1)

head, tail = s[:s.index("const D=")], s[s.index("\nconst esc="):]
HTML.write_text(head + "const D=" + json.dumps(D, ensure_ascii=False) + ";" + tail)
print("wrote", HTML, "agents:", list(ag))
