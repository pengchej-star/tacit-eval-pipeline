"""Build a standalone HTML page that walks one root-to-leaf path of a agent tree and shows, at every step,
the desiderata (checks) that decide which child to drill into.
Usage: python3 make_path_demo.py [agent=codex] [out.html]
Data comes from runs/<agent>/output/{tree,desiderata}.json and ../out/pooled_episode/2a_items.json.
CASE below is a hand-written reading of one episode (which checks hold in that case); everything else is read from the files."""
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
agent = sys.argv[1] if len(sys.argv) > 1 else "codex"
out = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "path_head_capacity.html"

PATH = ["T", "T.5", "T.5.2", "T.5.2.1"]
CASE_ITEM = "13848868:e2#1"
# node id -> {check index: what in this episode makes the check true}
CASE = {
    "T": {4: "A strong ResNeXt backbone with inputs already correct; the 5-fold ensemble sits at 0.93873 and the author says the gain must come from the model, not the data."},
    "T.5": {1: "The head is just global pooling then a linear layer, so it discards spatial / channel information the backbone already computes."},
    "T.5.2": {0: "The backbone feeds a minimal pool → linear head, so head capacity is the component to alter."},
}

tree = json.load(open(HERE / "runs" / agent / "output" / "tree.json"))
des = json.load(open(HERE / "runs" / agent / "output" / "desiderata.json"))["nodes"]
items = {i["id"]: i for i in json.load(open(HERE.parent / "out/pooled_episode/2a_items.json"))}


def find(n, i):
    if n["id"] == i:
        return n
    for c in n.get("children") or []:
        r = find(c, i)
        if r:
            return r


def card(n, selected):
    c = dict(id=n["id"], name=n["name"], sel=selected)
    if selected:
        c["desc"] = n.get("description", "")
        c["decision"] = n.get("decision", "")
        names = {k["id"]: k["name"] for k in n.get("children") or []}
        c["checks"] = []
        for g in (des.get(n["id"]) or {}).get("groups", []):
            for ch in g["checks"]:
                i = len(c["checks"])
                on = i in CASE.get(n["id"], {})
                c["checks"].append(dict(text=ch["check"], on=on, how=ch.get("how", "") if on else "",
                                        why=CASE.get(n["id"], {}).get(i, ""),
                                        pushes=[[names.get(k, k), v] for k, v in (ch.get("pushes") or {}).items()] if on else []))
    return c


cols = [dict(head="GOAL", cards=[card(find(tree, PATH[0]), True)])]
for k, nid in enumerate(PATH[:-1]):
    n = find(tree, nid)
    cols.append(dict(head=n.get("decision", ""), parent=nid,
                     cards=[card(c, c["id"] == PATH[k + 1]) for c in n["children"]]))
leaf = find(tree, PATH[-1])
cols.append(dict(head="Episodes filed under this leaf", parent=leaf["id"], cards=[
    dict(id=i, name=items[i]["comp"], sel=(i == CASE_ITEM), ctx=items[i]["instance"]["context"], act=items[i]["instance"]["action"], action=True)
    for i in leaf["items"]]))
data = dict(cols=cols, case=items[CASE_ITEM]["instance"]["context"])

TEMPLATE = r"""<!doctype html>
<html><head><meta charset="utf-8"><title>How we reach: __LEAF__</title>
<style>
:root{--maroon:#6b1320;--brown:#5a3e2b;--line:#e3d5c0;--beige:#f3e9db;--mute:#8a7a6a}
*{box-sizing:border-box}
body{margin:0;font:14px/1.45 -apple-system,"Segoe UI",sans-serif;color:#2a1f18;background:#fff}
main{padding:22px 28px 40px;min-width:1500px}
h1{font-size:20px;margin:0 0 2px}
.lead{color:var(--mute);margin:0 0 14px;max-width:900px}
.legend{display:flex;gap:22px;align-items:center;margin:0 0 18px;color:var(--brown)}
.legend i{display:inline-block;width:26px;height:14px;border-radius:4px;vertical-align:-2px;margin-right:6px}
.case{border:1px solid var(--line);border-left:4px solid #d97706;border-radius:6px;padding:8px 12px;margin:0 0 20px;max-width:1000px;font-size:13px}
.case b{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:#b45309;display:block}
#dg{position:relative;display:flex;gap:42px;align-items:flex-start}
svg{position:absolute;left:0;top:0;pointer-events:none;overflow:visible}
.col{width:300px;flex:none;position:relative;z-index:1}
.col>h3{margin:0 0 10px;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--brown);min-height:34px}
.card{background:#fff;border:1.5px solid var(--line);border-radius:10px;padding:10px 14px;margin:0 0 12px}
.card .nm{font-weight:600;font-size:15.5px}
.card.sel{border:2px solid var(--maroon);box-shadow:0 0 0 4px #f6dfe1}
.card .ds{color:var(--mute);margin-top:1px}
.card .sec{border-top:1px dashed var(--line);margin-top:8px;padding-top:7px}
.lab{font-size:11px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--brown);margin-right:5px}
.cks{list-style:none;margin:6px 0 0;padding:0}
.ck{position:relative;margin:5px 0;padding:1px 0 1px 24px;color:#4b3b30}
.ck::before{content:"☐";position:absolute;left:2px;top:1px;color:var(--mute)}
.ck.on::before{content:"✓";color:var(--maroon);font-weight:700}
.ck.on{background:#fdf2f3;padding:4px 7px 4px 24px;border-radius:5px;color:#2a1f18;font-weight:500}
.ck .sub{font-size:12.5px;color:var(--mute);margin-top:2px}
.ck .sub b{color:var(--brown)}
.ck .go{display:inline-block;font-size:11.5px;background:#f6dfe1;color:var(--maroon);border-radius:9px;padding:0 7px;margin:3px 4px 0 0}
.card.root{background:var(--maroon);border-color:var(--maroon);color:#fff}
.card.root .ds,.card.root .lab{color:#e9c9cd}
.card.root .sec{border-color:#9a4a55}
.card.root .ck{color:#f3dde0}
.card.root .ck::before{color:#e9c9cd}.card.root .ck.on::before{color:#fff}.card.root .ck.on{background:#8a2a38;color:#fff}
.card.root .ck .sub{color:#ecd0d4}.card.root .ck .sub b{color:#fff}
.card.root .ck .go{background:#fff;color:var(--maroon)}
.card.act{background:var(--beige);border-color:var(--line);padding:9px 13px}
.card.act .nm{font-size:13.5px}
.card.act.sel{border:2px solid var(--maroon)}
.card.act .eid{font-size:12px;color:var(--mute);margin-top:1px}
.card.act.sel .eid{color:var(--maroon);font-weight:600}
.card.act .ds{font-size:12.5px;color:#4b3b30}
.card.act .ds p{margin:4px 0 0}
</style></head><body><main>
<h1>How we reach “__LEAF__”</h1>
<p class="lead">Each column is one decision, titled by its question. The highlighted card is the branch taken. In the selected cards, the desiderata are listed as bullets: ✓ marks a check that holds in this case and decides the branch, ☐ marks a check that was considered but does not hold (name only).</p>
<div class="legend"><span><i style="border:2px solid var(--maroon);box-shadow:0 0 0 3px #f6dfe1"></i>selected</span><span><i style="background:var(--beige);border:1.5px solid var(--line)"></i>episode (bottom of the tree)</span></div>
<div class="case"><b>The case we walk through</b><span id="casetxt"></span></div>
<div id="dg"><svg id="sv"></svg></div>
<p class="lead" style="margin-top:16px;font-size:12.5px">Desiderata names, “how to verify” text and branch weights come from the __AGENT__ tree’s <code>desiderata.json</code>. Which checks are highlighted, and the “In this case” lines, are a reading of the episode and are illustrative.</p>
</main>
<script>
const D=__DATA__;
const esc=s=>String(s??'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
document.getElementById('casetxt').textContent=D.case;
const dg=document.getElementById('dg');
D.cols.forEach((col,ci)=>{
 const el=document.createElement('div');el.className='col';
 el.innerHTML=`<h3>${esc(col.head)}</h3>`+col.cards.map(c=>{
  const root=ci==0;
  if(c.action){
   return `<div class="card act ${c.sel?'sel':''}" data-id="${esc(c.id)}"><div class="nm">${esc(c.name)}</div>
    <div class="eid">${esc(c.id)}${c.sel?' · the case walked through':''}</div>
    <div class="ds"><p><span class="lab">Context</span>${esc(c.ctx)}</p><p><span class="lab">Action</span>${esc(c.act)}</p></div></div>`}
  if(!c.sel)return `<div class="card" data-id="${esc(c.id)}"><div class="nm">${esc(c.name)}</div></div>`;
  let h=`<div class="card sel ${root?'root':''}" data-id="${esc(c.id)}"><div class="nm">${esc(c.name)}</div><div class="ds">${esc(c.desc)}</div>`;
  if(c.decision)h+=`<div class="sec"><span class="lab">Next decision</span>${esc(c.decision)}</div>`;
  if(c.checks&&c.checks.length)h+=`<div class="sec"><span class="lab">Desiderata</span><ul class="cks">`+c.checks.map(k=>
   `<li class="ck ${k.on?'on':''}">${esc(k.text)}`+(k.on?`<div class="sub"><b>How to verify:</b> ${esc(k.how)}</div>`+(k.why?`<div class="sub"><b>In this case:</b> ${esc(k.why)}</div>`:'')+
    `<div>${k.pushes.map(p=>`<span class="go">${esc(p[0])} ${p[1]>0?'+':''}${p[1]}</span>`).join('')}</div>`:'')+`</li>`).join('')+`</ul></div>`;
  return h+`</div>`}).join('');
 dg.appendChild(el);
});
function draw(){
 const sv=document.getElementById('sv'),b=dg.getBoundingClientRect();sv.setAttribute('width',b.width);sv.setAttribute('height',b.height);
 let p='';
 D.cols.forEach((col,ci)=>{if(!col.parent)return;
  const pc=dg.children[ci].querySelector('.card.sel');if(!pc)return;
  const r=pc.getBoundingClientRect(),x1=r.right-b.left,y1=r.top+Math.min(40,r.height/2)-b.top;
  dg.children[ci+1].querySelectorAll('.card').forEach(k=>{
   const q=k.getBoundingClientRect(),x2=q.left-b.left,y2=q.top+22-b.top,m=(x1+x2)/2;
   const sel=k.classList.contains('sel');
   p+=`<path d="M${x1},${y1} C${m},${y1} ${m},${y2} ${x2},${y2}" fill="none" stroke="${sel?'#6b1320':'#e3d5c0'}" stroke-width="${sel?2:1.5}"/>`;
  });
 });
 sv.innerHTML=p;
}
draw();addEventListener('resize',draw);addEventListener('load',draw);
</script></body></html>"""

html = (TEMPLATE.replace("__LEAF__", leaf["name"]).replace("__AGENT__", agent)
        .replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")))
out.write_text(html)
print("wrote", out)
