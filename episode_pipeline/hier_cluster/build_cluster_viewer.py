"""Self-contained html viewer for the goal -> context -> action clusters of the flat episode items.

    python build_cluster_viewer.py            # -> ../results/cluster_viewer.html

Reads hier_flat_items.json (tree), hier_flat_items_summaries.json (LLM titles/summaries) and ../results/episode_items.jsonl (instance + general text).
"""
import argparse, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / "results"

PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Goal / context / action clusters</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{--bg:#f6f7f9;--panel:#fff;--ink:#1c2230;--muted:#667085;--line:#e3e6ec;--accent:#2563eb;--accent-soft:#e8effd;--cent:#b45309;--cent-soft:#fdf1dc;--hit:#fff3a8;--inst:#f3f4f6}
@media (prefers-color-scheme:dark){:root{--bg:#12151b;--panel:#1a1f28;--ink:#e6e9ef;--muted:#9aa3b2;--line:#2b3240;--accent:#7aa2ff;--accent-soft:#1f2a44;--cent:#f2b45a;--cent-soft:#3a2d17;--hit:#5a4d10;--inst:#232a36}}
*{box-sizing:border-box}html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;display:flex;flex-direction:column}
header{background:var(--panel);border-bottom:1px solid var(--line);padding:10px 16px;display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center}
h1{font-size:16px;margin:0 8px 0 0;font-weight:650}
label.ctl{display:flex;gap:6px;align-items:center;color:var(--muted);font-size:13px}
input[type=search],input[type=number],select{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:6px;padding:5px 8px;font:inherit;max-width:230px}
input[type=search]{width:300px}input[type=number]{width:64px}
#stats{margin-left:auto;color:var(--muted);font-size:13px}
main{flex:1;min-height:0;display:grid;grid-template-columns:minmax(320px,420px) 1fr}
#list{overflow:auto;border-right:1px solid var(--line);background:var(--panel)}
.row{padding:9px 14px;border-bottom:1px solid var(--line);cursor:pointer}
.row:hover{background:var(--accent-soft)}.row.sel{background:var(--accent-soft);box-shadow:inset 3px 0 0 var(--accent)}
.row .g{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;font-weight:600}
.meta{display:flex;flex-wrap:wrap;gap:4px 8px;color:var(--muted);font-size:12px;margin-top:3px}
.pill{background:var(--accent-soft);color:var(--accent);border-radius:999px;padding:0 8px;font-size:12px;font-weight:600}
#detail{overflow:auto;padding:18px 24px 60px}
.empty{color:var(--muted);padding:40px;text-align:center}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin-bottom:14px}
.label{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);font-weight:650;margin-bottom:2px}
.cent{border-left:3px solid var(--cent);background:var(--cent-soft);border-radius:6px;padding:8px 12px;margin:6px 0}.cent .label{color:var(--cent)}
.acc{border-left:3px solid var(--accent);background:var(--accent-soft);border-radius:6px;padding:8px 12px;margin:6px 0}.acc .label{color:var(--accent)}
.big{font-size:17px;font-weight:650}.muted{color:var(--muted)}
.kv{display:flex;flex-wrap:wrap;gap:6px 22px;margin:8px 0;font-size:13px}
h3{font-size:14px;margin:22px 0 8px}
details{border:1px solid var(--line);border-radius:8px;margin:8px 0;background:var(--panel)}
details>summary{cursor:pointer;padding:8px 12px;list-style:none;display:flex;flex-wrap:wrap;gap:4px 10px;align-items:baseline}
details>summary::-webkit-details-marker{display:none}
details>summary::before{content:"▸";color:var(--muted)}details[open]>summary::before{content:"▾"}
details.ctx>summary{font-weight:600}
details.act{margin:6px 0 6px 14px;background:transparent}
details.item{margin:6px 0 6px 14px}
.body{padding:4px 14px 12px;border-top:1px solid var(--line);display:grid;gap:8px}.body p{margin:0}
.inst{background:var(--inst);border-radius:6px;padding:8px 12px}
code{font-size:12px;color:var(--muted)}
mark{background:var(--hit);color:inherit}
.togg{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:8px;padding:6px 12px;cursor:pointer;font:inherit}
ul{margin:4px 0;padding-left:20px}
</style></head><body>
<header>
  <h1>Goal / context / action clusters</h1>
  <input type="search" id="q" placeholder="Search text or ID (e.g. 13848868:e1#1, g9, g9.c1)">
  <label class="ctl">Competition <select id="comp"><option value="">all</option></select></label>
  <label class="ctl">Min kernels <input type="number" id="mk" min="1" value="1"></label>
  <label class="ctl">Sort <select id="sort"><option value="items"># items</option><option value="kernels"># kernels</option><option value="ctx"># contexts</option></select></label>
  <button class="togg" id="expand">Expand all</button>
  <span id="stats"></span>
</header>
<main><div id="list"></div><div id="detail"><div class="empty">Pick a goal cluster on the left.</div></div></main>
<script id="data" type="application/json">__DATA__</script>
<script>
const D=JSON.parse(document.getElementById('data').textContent);
const $=id=>document.getElementById(id);
function h(tag,attrs,...kids){const e=document.createElement(tag);for(const[k,v]of Object.entries(attrs||{})){if(k==='class')e.className=v;else if(k.startsWith('on'))e.addEventListener(k.slice(2),v);else e.setAttribute(k,v)}
  for(const c of kids.flat()){if(c==null||c===false)continue;e.append(c.nodeType?c:document.createTextNode(String(c)))}return e}
const short=c=>(c||'').replace(/-prediction|-challenge|-classification|-detection|-survival-predictions|readabilityprize|learning-agency-lab-|-clip-catheter-line/g,'');
const field=(label,txt,cls)=>txt?h('div',{class:cls||''},h('div',{class:'label'},label),h('div',{},txt)):null;
const comps=[...new Set(Object.values(D.items).map(i=>i.comp))].sort();
$('comp').append(...comps.map(c=>h('option',{value:c},short(c))));
let sel=null,expandAll=false,target=null;
const idKey=Object.fromEntries(Object.keys(D.items).map(i=>[i.toLowerCase(),i]));
function setTarget(){const q=$('q').value.trim().toLowerCase();target=idKey[q]||null;
  if(target){const g=D.goals.find(g=>g.ids.includes(target));if(g)sel=g.id}}
// per goal cluster: all item ids and a lowercase search blob
D.goals.forEach((g,gi)=>{g.children.forEach((c,cj)=>c.id=g.id+'.c'+cj);g.ids=g.children.flatMap(c=>c.children.flatMap(a=>a.items));g.comps=new Set(g.ids.map(i=>D.items[i].comp));
  g._t=(g.id+' '+g.ids.join(' ')+' '+g.children.map(c=>c.id).join(' ')+' '+g.title+' '+g.summary+' '+g.children.map(c=>c.title+' '+c.summary+' '+c.typical_actions).join(' ')+' '+g.ids.map(i=>{const x=D.items[i].general;return x.goal+' '+x.context+' '+x.action}).join(' ')).toLowerCase()});
function cur(){const q=$('q').value.toLowerCase().trim(),comp=$('comp').value,mk=+$('mk').value||1,s=$('sort').value;
  const a=D.goals.filter(g=>(!q||g._t.includes(q))&&(!comp||g.comps.has(comp))&&g.n_kernels>=mk);
  a.sort((x,y)=>s==='kernels'?y.n_kernels-x.n_kernels:s==='ctx'?y.children.length-x.children.length:y.n_items-x.n_items);return a}
let tm=null;
['q','comp','mk','sort'].forEach(i=>$(i).addEventListener('input',()=>{clearTimeout(tm);tm=setTimeout(()=>{sel=null;setTarget();render()},200)}));
$('expand').onclick=()=>{expandAll=!expandAll;$('expand').textContent=expandAll?'Collapse all':'Expand all';render()};
function hl(txt){const q=$('q').value.trim();if(!q||!txt)return txt;const i=txt.toLowerCase().indexOf(q.toLowerCase());if(i<0)return txt;
  return [txt.slice(0,i),h('mark',{},txt.slice(i,i+q.length)),txt.slice(i+q.length)]}
function itemBox(id){const it=D.items[id],g=it.general,x=it.instance;
  return h('details',Object.assign({class:'item'},id===target?{open:'',id:'target'}:{}),h('summary',{},h('span',{},hl(g.goal)),h('code',{},id)),
    h('div',{class:'body'},field('General goal',g.goal),field('General context',g.context,'cent'),field('General action',g.action,'acc'),
      h('div',{class:'inst'},h('div',{class:'label'},`Instance · ${short(it.comp)} · ${it.tier} · ${it.ep.pattern} v${it.ep.start_v}-v${it.ep.end_v}`),
        h('p',{},h('b',{},'Goal: '),x.goal),h('p',{},h('b',{},'Context: '),x.context),h('p',{},h('b',{},'Action: '),x.action),
        h('div',{class:'muted'},'id: '+id+' · steps: '+(it.steps||[]).join(', ')))))}
function actBox(a){return h('details',Object.assign({class:'act'},expandAll||a.items.includes(target)?{open:''}:{}),
  h('summary',{},h('span',{},hl(a.representative)),h('span',{class:'pill'},a.n_items+' items'),h('span',{class:'muted'},a.n_kernels+' kernels')),
  h('div',{class:'body'},a.items.map(itemBox)))}
function ctxBox(c){return h('details',Object.assign({class:'ctx'},expandAll||c.children.some(a=>a.items.includes(target))?{open:''}:{}),
  h('summary',{},h('span',{},hl(c.title)),h('code',{},c.id),h('span',{class:'pill'},c.n_items+' items'),h('span',{class:'muted'},`${c.n_kernels} kernels · ${c.children.length} action groups`)),
  h('div',{class:'body'},field('Situation',c.summary,'cent'),field('Typical actions',c.typical_actions,'acc'),
    h('div',{class:'label'},'Action groups (near-duplicate actions merged)'),c.children.map(actBox)))}
function pick(id){sel=id;document.querySelectorAll('#list .row').forEach(r=>r.classList.toggle('sel',r.dataset.id===id));showDetail(cur())}
function render(){const a=cur();$('stats').textContent=`${a.length} / ${D.goals.length} goal clusters · ${D.n_items} items · ${D.n_ctx} context clusters`;
  $('list').replaceChildren(...a.map(g=>h('div',{class:'row'+(sel===g.id?' sel':''),'data-id':g.id,onclick:()=>pick(g.id)},
    h('div',{class:'g'},g.title),h('div',{class:'meta'},h('span',{class:'pill'},g.id),`${g.n_items} items · ${g.n_kernels} kernels · ${g.children.length} contexts`))));
  showDetail(a)}
function showDetail(a){const g=a.find(x=>x.id===sel),d=$('detail');
  d.replaceChildren(g?h('div',{},h('div',{class:'card'},h('div',{class:'big'},g.title),
      h('div',{class:'kv'},h('span',{class:'pill'},g.id),h('span',{},`${g.n_items} items · ${g.n_kernels} kernels · ${g.comps.size} competitions`)),
      field('Summary',g.summary,'cent'),field('Representative goal',g.representative)),
    h('h3',{},`Contexts (${g.children.length})`),g.children.map(ctxBox)):h('div',{class:'empty'},'Pick a goal cluster on the left.'));
  const t=document.getElementById('target');if(t)t.scrollIntoView({block:'center'})}
render();
</script></body></html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE.parent / "results" / "cluster_viewer.html"))
    a = ap.parse_args()
    tree = json.load(open(RES / "hier_flat_items.json", encoding="utf-8"))["tree"]
    summ = json.load(open(RES / "hier_flat_items_summaries.json", encoding="utf-8"))
    items = {}
    for l in open(HERE.parent / "results" / "episode_items.jsonl", encoding="utf-8"):
        r = json.loads(l)
        for n, it in enumerate(r.get("items") or [], 1):
            items[f"{r['ep_id']}#{n}"] = dict(comp=r["comp"], tier=r["tier"] if isinstance(r["tier"], str) else "unknown", ep={k: r["episode"][k] for k in ("start_v", "end_v", "pattern")},
                                              steps=it.get("steps") or [], instance=it.get("instance") or {}, general=it.get("general") or {})
    goals, n_ctx = [], 0
    for gi, g in enumerate(tree):
        s = summ["goal"].get(f"g{gi}", {})
        node = dict(id=f"g{gi}", title=s.get("title") or g["representative"], summary=s.get("summary") or "", representative=g["representative"],
                    n_items=g["n_items"], n_kernels=g["n_kernels"], children=[])
        for cj, c in enumerate(g["children"]):
            cs = summ["context"].get(f"g{gi}.c{cj}", {})
            node["children"].append(dict(title=cs.get("title") or c["representative"], summary=cs.get("summary") or "", typical_actions=cs.get("typical_actions") or "",
                                         n_items=c["n_items"], n_kernels=c["n_kernels"],
                                         children=[dict(representative=ac["representative"], n_items=ac["n_items"], n_kernels=ac["n_kernels"], items=ac["items"]) for ac in c["children"]]))
            n_ctx += 1
        goals.append(node)
    data = json.dumps(dict(goals=goals, items=items, n_items=len(items), n_ctx=n_ctx), ensure_ascii=False, allow_nan=False).replace("</", "<\\/")
    Path(a.out).write_text(PAGE.replace("__DATA__", data), encoding="utf-8")
    print(f"{len(goals)} goal clusters, {n_ctx} context clusters, {len(items)} items -> {a.out}")


if __name__ == "__main__":
    main()
