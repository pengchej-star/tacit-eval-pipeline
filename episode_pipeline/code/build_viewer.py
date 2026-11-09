"""Build a self-contained html viewer for the extracted knowledge (episode_pipeline/results).

    python build_viewer.py                      # -> ../results/knowledge_viewer.html
    python build_viewer.py --runnable-csv PATH  # csv with runnable, key_id, v_k, v_k1 (default: ../../tacit-eval-pipeline/triage/runnable_cases.csv)

Four views:
  Rules           knowledge_full.json    cross-expert rules (the clustered result), with the episode items that support each
  Episodes        episode_rationales     episode-level search process / feedback response / exit and the L2/L3 items, per episode
  Steps           runnable.jsonl         step-level rationale reconstruction of the 7 runnable steps (consensus of the samples)
  Step clusters   clusters_runnable.json LLM clustering of those step-level items: goal -> lever context -> lever -> action
Item ids link the views: rule.support -> episode item '<kernel>:e<n>#<k>'; cluster sources -> step item '<key>:<v_old>-><v_new>#<k>'.
"""
import argparse, csv, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE.parent / "results"


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def clean(x):
    """NaN is not valid JSON (some rule examples carry a NaN tier)."""
    if isinstance(x, float) and x != x:
        return None
    if isinstance(x, dict):
        return {k: clean(v) for k, v in x.items()}
    if isinstance(x, list):
        return [clean(v) for v in x]
    return x


def load(runnable_csv):
    run_pairs = set()
    if runnable_csv and Path(runnable_csv).exists():
        for r in csv.DictReader(open(runnable_csv, encoding="utf-8")):
            if r["runnable"] == "True":
                run_pairs.add(f"{r['key_id']}:{r['v_k']}->{r['v_k1']}")
    rules = json.load(open(RES / "knowledge_full.json", encoding="utf-8"))["rules"]
    cited = {}
    for i, r in enumerate(rules):
        for s in r["support"]:
            cited.setdefault(s, []).append(i)
    eps = []
    for r in jl(RES / "episode_rationales.jsonl"):
        e = r["episode"]
        items = []
        for k, it in enumerate(r.get("rationales") or [], 1):
            iid = f"{r['ep_id']}#{k}"
            items.append({**it, "id": iid, "rules": cited.get(iid, [])})
        eps.append(dict(id=r["ep_id"], key=r["key_id"], comp=r["comp"], tier=r["tier"], ep=e, items=items,
                        search_process=r.get("search_process"), feedback_response=r.get("feedback_response"), exit=r.get("exit"),
                        unseen=r.get("relied_on_unseen"), evidence=r.get("evidence"), confidence=r.get("confidence"),
                        runnable=sorted(set(e["step_ids"]) & run_pairs)))
    steps = []
    for r in jl(RES / "runnable.jsonl"):
        steps.append(dict(id=r["step_id"], comp=r["comp"], goal=r["goal"], consensus=r["consensus"], n_samples=len(r["samples"]),
                          agreement=r.get("agreement"), disagreements=r.get("disagreements"), plausible=r.get("plausible"),
                          plausibility_note=r.get("plausibility_note")))
    chunks = json.load(open(RES / "clusters_runnable.json", encoding="utf-8"))["chunks"]
    return dict(rules=rules, eps=eps, steps=steps, chunks=chunks, n_run_pairs=len(run_pairs))


PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Episode-level tacit knowledge</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{--bg:#f6f7f9;--panel:#fff;--ink:#1c2230;--muted:#667085;--line:#e3e6ec;--accent:#2563eb;--accent-soft:#e8effd;--cent:#b45309;--cent-soft:#fdf1dc;--hit:#fff3a8;--run:#0f9d58;--run-soft:#e7f6ed}
@media (prefers-color-scheme:dark){:root{--bg:#12151b;--panel:#1a1f28;--ink:#e6e9ef;--muted:#9aa3b2;--line:#2b3240;--accent:#7aa2ff;--accent-soft:#1f2a44;--cent:#f2b45a;--cent-soft:#3a2d17;--hit:#5a4d10;--run:#34b374;--run-soft:#16301f}}
*{box-sizing:border-box}html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;display:flex;flex-direction:column}
header{background:var(--panel);border-bottom:1px solid var(--line);padding:10px 16px;display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center}
h1{font-size:16px;margin:0 8px 0 0;font-weight:650}
.tabs{display:flex;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.tabs button{border:0;background:transparent;color:var(--ink);padding:6px 12px;cursor:pointer;font:inherit}
.tabs button.on{background:var(--accent);color:#fff}
label.ctl{display:flex;gap:6px;align-items:center;color:var(--muted);font-size:13px}
input[type=search],input[type=number],select{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:6px;padding:5px 8px;font:inherit;max-width:230px}
input[type=search]{width:300px}input[type=number]{width:64px}
#stats{margin-left:auto;color:var(--muted);font-size:13px}
main{flex:1;min-height:0;display:grid;grid-template-columns:minmax(300px,400px) 1fr}
#list{overflow:auto;border-right:1px solid var(--line);background:var(--panel)}
.row{padding:9px 14px;border-bottom:1px solid var(--line);cursor:pointer}
.row:hover{background:var(--accent-soft)}.row.sel{background:var(--accent-soft);box-shadow:inset 3px 0 0 var(--accent)}
.row .g{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.meta{display:flex;flex-wrap:wrap;gap:4px 8px;color:var(--muted);font-size:12px;margin-top:3px}
.pill{background:var(--accent-soft);color:var(--accent);border-radius:999px;padding:0 8px;font-size:12px;font-weight:600}
.pill.run{background:var(--run);color:#fff}.pill.l3{background:var(--cent);color:#fff}
#detail{overflow:auto;padding:18px 24px 60px}
.empty{color:var(--muted);padding:40px;text-align:center}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin-bottom:14px}
.label{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);font-weight:650;margin-bottom:2px}
.cent{border-left:3px solid var(--cent);background:var(--cent-soft);border-radius:6px;padding:8px 12px;margin:6px 0}
.cent .label{color:var(--cent)}
.acc{border-left:3px solid var(--accent);background:var(--accent-soft);border-radius:6px;padding:8px 12px;margin:6px 0}
.acc .label{color:var(--accent)}
.big{font-size:16px;font-weight:600}.muted{color:var(--muted)}
.kv{display:flex;flex-wrap:wrap;gap:6px 22px;margin-top:10px;font-size:13px}
.bars{margin-top:10px;display:grid;grid-template-columns:auto 1fr auto;gap:3px 8px;align-items:center;font-size:12px}
.bar{height:8px;background:var(--accent);border-radius:4px;min-width:2px}
h3{font-size:14px;margin:22px 0 8px}
details.item{border:1px solid var(--line);border-radius:8px;margin:6px 0;background:var(--panel)}
details.item>summary{cursor:pointer;padding:7px 12px;list-style:none;display:flex;flex-wrap:wrap;gap:4px 10px;align-items:baseline}
details.item>summary::-webkit-details-marker{display:none}
details.item>summary::before{content:"▸";color:var(--muted)}details.item[open]>summary::before{content:"▾"}
details.item.run{border-left:4px solid var(--run);background:var(--run-soft)}
.sum-goal{flex:1 1 320px}
.tag{font-size:11px;border-radius:4px;padding:0 6px;font-weight:650;background:var(--accent);color:#fff}.tag.l3{background:var(--cent)}
code{font-size:12px;color:var(--muted)}
a.lnk{color:var(--accent);cursor:pointer;text-decoration:underline;font-size:12px;font-family:ui-monospace,Menlo,monospace}
.body{padding:4px 14px 12px;border-top:1px solid var(--line);display:grid;gap:8px}.body p{margin:0}
.togg{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:8px;padding:6px 12px;cursor:pointer;font:inherit}
.togg.on{background:var(--run);border-color:var(--run);color:#fff}
.indent{margin-left:18px;padding-left:10px;border-left:2px dashed var(--line)}
ul{margin:4px 0;padding-left:20px}
</style></head><body>
<header>
  <h1>Episode-level tacit knowledge</h1>
  <div class="tabs" id="tabs"><button data-m="rules" class="on">Rules</button><button data-m="eps">Episodes</button><button data-m="steps">Steps</button><button data-m="chunks">Step clusters</button></div>
  <input type="search" id="q" placeholder="Search text">
  <button class="togg" id="runonly" title="Only entries touching a runnable=True version pair of runnable_cases.csv">Runnable cases only</button>
  <label class="ctl">Competition <select id="comp"><option value="">all</option></select></label>
  <label class="ctl" id="f1l">Level <select id="f1"></select></label>
  <label class="ctl" id="f2l">Min kernels <input type="number" id="f2" min="1" value="2"></label>
  <label class="ctl">Sort <select id="sort"></select></label>
  <span id="stats"></span>
</header>
<main><div id="list"></div><div id="detail"><div class="empty">Pick an entry on the left.</div></div></main>
<script id="data" type="application/json">__DATA__</script>
<script>
const D=JSON.parse(document.getElementById('data').textContent);
const $=id=>document.getElementById(id);
function h(tag,attrs,...kids){const e=document.createElement(tag);for(const[k,v]of Object.entries(attrs||{})){if(k==='class')e.className=v;else if(k.startsWith('on'))e.addEventListener(k.slice(2),v);else e.setAttribute(k,v)}
  for(const c of kids.flat()){if(c==null||c===false)continue;e.append(c.nodeType?c:document.createTextNode(String(c)))}return e}
const short=c=>(c||'').replace(/-prediction|-challenge|-classification|-detection|-survival-predictions|readabilityprize|learning-agency-lab-|-clip-catheter-line/g,'');
const comps=[...new Set(D.eps.map(e=>e.comp))].sort();
$('comp').append(...comps.map(c=>h('option',{value:c},short(c))));
const epById=Object.fromEntries(D.eps.map(e=>[e.id,e]));
const itemEp={};D.eps.forEach(e=>e.items.forEach(i=>itemEp[i.id]=e));
const stepById=Object.fromEntries(D.steps.map(s=>[s.id,s]));
let mode='rules',sel=null,runOnly=false;
const SORTS={rules:[['kernels','# kernels'],['items','# items'],['new','% new best']],eps:[['order','trajectory order'],['len','# transitions'],['items','# items']],steps:[['order','order']],chunks:[['size','# items']]};
function setMode(m){mode=m;sel=null;document.querySelectorAll('#tabs button').forEach(b=>b.classList.toggle('on',b.dataset.m===m));
  $('sort').replaceChildren(...SORTS[m].map(([v,t])=>h('option',{value:v},t)));
  const f1=$('f1'),f1l=$('f1l'),f2l=$('f2l');
  f1l.style.display=(m==='rules'||m==='eps')?'':'none';f2l.style.display=m==='rules'?'':'none';
  if(m==='rules')f1.replaceChildren(...[['','all'],['L2','L2 method'],['L3','L3 strategy']].map(([v,t])=>h('option',{value:v},t)));
  if(m==='eps')f1.replaceChildren(...[['','all patterns'],...['sweep','probe','revert','build','fix','consolidate','explore'].map(p=>[p,p])].map(([v,t])=>h('option',{value:v},t)));
  $('comp').parentElement.style.display=(m==='chunks')?'none':'';
  render()}
document.querySelectorAll('#tabs button').forEach(b=>b.onclick=()=>setMode(b.dataset.m));
['q','comp','f1','f2','sort'].forEach(i=>$(i).addEventListener('input',()=>{sel=null;render()}));
$('runonly').onclick=()=>{runOnly=!runOnly;$('runonly').classList.toggle('on',runOnly);sel=null;render()};
function go(m,id){setMode(m);const arr=cur();const i=arr.findIndex(x=>x.id===id||x._i===id);if(i<0){$('q').value='';$('comp').value='';runOnly=false;$('runonly').classList.remove('on');$('f1').value='';$('f2').value=1;render()}
  sel=id;render();const r=document.querySelector('.row.sel');if(r)r.scrollIntoView({block:'center'})}
function bars(obj,total){const g=h('div',{class:'bars'});for(const[k,v]of Object.entries(obj).sort((a,b)=>b[1]-a[1]))g.append(h('span',{},k),h('div',{class:'bar',style:`width:${Math.max(2,100*v/total)}%`}),h('span',{},v));return g}
function lnk(m,id,txt){return h('a',{class:'lnk',onclick:()=>go(m,id)},txt||id)}
function field(label,txt,cls){return txt?h('div',{class:cls||''},h('div',{class:'label'},label),h('div',{},txt)):null}
const blob=x=>JSON.stringify(x).toLowerCase();
D.rules.forEach((r,i)=>{r._i=i;r.id=String(i);r._t=blob([r.name,r.context,r.action,r.exceptions,r.merged_from]);r._run=(r.support||[]).some(s=>itemEp[s]&&itemEp[s].runnable.length)});
D.eps.forEach(e=>{e._t=blob([e.ep,e.search_process,e.feedback_response,e.exit,e.items.map(i=>[i.goal,i.lever,i.action,i.action_context,i.lever_context])])});
D.steps.forEach(s=>{s._run=true;s._t=blob([s.goal,s.consensus])});
D.chunks.forEach((c,i)=>{c._i=i;c.id='c'+i;c._t=blob(c);c._run=true});
function cur(){const q=$('q').value.toLowerCase().trim(),comp=$('comp').value,f1=$('f1').value,f2=+$('f2').value||1,s=$('sort').value;
  let a;
  if(mode==='rules'){a=D.rules.filter(r=>(!q||r._t.includes(q))&&(!comp||r.comps.includes(comp))&&(!f1||r.level===f1)&&r.kernels.length>=f2&&(!runOnly||r._run));
    const nb=r=>(r.new_best.yes||0)/Math.max(1,(r.new_best.yes||0)+(r.new_best.no||0));
    a.sort((x,y)=>s==='items'?y.n_items-x.n_items:s==='new'?nb(y)-nb(x):y.kernels.length-x.kernels.length||y.n_items-x.n_items)}
  else if(mode==='eps'){a=D.eps.filter(e=>(!q||e._t.includes(q))&&(!comp||e.comp===comp)&&(!f1||e.ep.pattern===f1)&&(!runOnly||e.runnable.length));
    if(s==='len')a.sort((x,y)=>y.ep.n_transitions-x.ep.n_transitions);else if(s==='items')a.sort((x,y)=>y.items.length-x.items.length)}
  else if(mode==='steps')a=D.steps.filter(r=>(!q||r._t.includes(q))&&(!comp||r.comp===comp));
  else{a=D.chunks.filter(c=>!q||c._t.includes(q));a.sort((x,y)=>y.ids.length-x.ids.length)}
  return a}
function render(){const a=cur();$('stats').textContent=`${a.length} shown`+(mode==='eps'?` · ${D.eps.length} episodes`:mode==='rules'?` · ${D.rules.length} rules`:'')+` · ${D.n_run_pairs} runnable pairs`;
  const L=$('list');L.replaceChildren(...a.slice(0,600).map(x=>{
    let top,meta;
    if(mode==='rules'){top=h('div',{class:'g'},x.name.replace(/_/g,' '));meta=[h('span',{class:'pill'+(x.level==='L3'?' l3':'')},x.level),`${x.kernels.length} kernels · ${x.comps.length} comps · ${x.n_items} items`,x._run&&h('span',{class:'pill run'},'runnable')]}
    else if(mode==='eps'){top=h('div',{class:'g'},x.ep.objective);meta=[h('span',{class:'pill'},x.ep.pattern||'?'),`${x.id} · ${short(x.comp)} · v${x.ep.start_v}-v${x.ep.end_v} · ${x.items.length} items`,x.runnable.length&&h('span',{class:'pill run'},'runnable')]}
    else if(mode==='steps'){top=h('div',{class:'g'},x.goal);meta=[x.id,short(x.comp)]}
    else{top=h('div',{class:'g'},x.goal);meta=[`${x.ids.length} items · ${x.lever_contexts.length} lever contexts`]}
    return h('div',{class:'row'+(sel===x.id?' sel':''),onclick:()=>{sel=x.id;render()}},top,h('div',{class:'meta'},meta))}));
  if(a.length>600)L.append(h('div',{class:'empty'},`first 600 of ${a.length}; refine filters`));
  const x=a.find(y=>y.id===sel);const d=$('detail');d.replaceChildren(x?({rules:dRule,eps:dEp,steps:dStep,chunks:dChunk}[mode])(x):h('div',{class:'empty'},'Pick an entry on the left.'))}
function itemBox(it,open){return h('details',Object.assign({class:'item'+(it.runnable?' run':'')},open?{open:''}:{}),
  h('summary',{},h('span',{class:'tag'+(it.level==='L3'?' l3':'')},it.level||'item'),h('span',{class:'sum-goal'},it.goal),h('code',{},it.id)),
  h('div',{class:'body'},field('Lever context',it.lever_context,'cent'),field('Lever',it.lever),field('Action context',it.action_context,'acc'),field('Action',it.action),field('Counter-evidence',it.counter_evidence),
    it.instances&&h('div',{},h('span',{class:'label'},'Instances '),it.instances.map(s=>[h('code',{},s),' '])),
    it.rules&&it.rules.length&&h('div',{},h('span',{class:'label'},'Cited by rules '),it.rules.map(r=>[lnk('rules',String(r),D.rules[r].name),' ']))))}
function dRule(r){const nb=(r.new_best.yes||0)+(r.new_best.no||0);
  const n=h('div',{},h('div',{class:'card'},h('div',{class:'big'},r.name.replace(/_/g,' ')),
    h('div',{class:'kv'},h('span',{},h('span',{class:'pill'+(r.level==='L3'?' l3':'')},r.level)),h('span',{},`${r.kernels.length} kernels, ${r.comps.length} competitions, ${r.n_items} items`),
      h('span',{},`episodes reaching a new best: ${r.new_best.yes||0}/${nb}`),h('span',{class:'muted'},'cells: '+(r.cells||[]).join(', '))),
    field('Context (when it applies)',r.context,'cent'),field('Action',r.action,'acc'),field('Exceptions',r.exceptions),
    r.merged_from&&r.merged_from.length>1&&h('div',{class:'muted'},'merged from: '+r.merged_from.join(', ')),
    h('div',{class:'label',style:'margin-top:10px'},'Expert tiers'),bars(r.tiers,r.n_items),h('div',{class:'label',style:'margin-top:10px'},'Competitions'),h('div',{},r.comps.map(short).join(', '))),
    h('h3',{},`Supporting episode items (${r.support.length})`));
  r.support.forEach(s=>{const e=itemEp[s];const it=e&&e.items.find(i=>i.id===s);
    n.append(it?h('div',{},h('div',{class:'meta'},lnk('eps',e.id,'open episode '+e.id),`${short(e.comp)} · ${e.tier} · ${e.ep.pattern} · v${e.ep.start_v}-v${e.ep.end_v}`,e.runnable.length&&h('span',{class:'pill run'},'runnable')),itemBox({...it,runnable:e.runnable.length},false)):h('div',{},h('code',{},s)))});
  return n}
function dEp(e){const x=e.ep;const n=h('div',{},h('div',{class:'card'},h('div',{class:'big'},x.objective),
  h('div',{class:'kv'},h('span',{class:'pill'},x.pattern||'?'),h('span',{},`${e.id} · ${e.comp} · ${e.tier}`),h('span',{},`v${x.start_v}→v${x.end_v}, ${x.n_transitions} transitions, ${x.n_scored} scored`),h('span',{},`confidence ${e.confidence}`)),
  h('div',{class:'kv'},h('span',{},'lever: '+(x.lever||'-')),h('span',{},'trigger: '+(x.trigger||'-'))),field('Outcome',x.outcome),
  x.scores&&x.scores.length&&h('div',{class:'muted'},'LB scores: '+x.scores.join(' → ')),
  e.runnable.length&&h('div',{},h('span',{class:'pill run'},'runnable pairs'),' ',e.runnable.map(s=>[h('code',{},s),' '])),
  h('div',{style:'margin-top:8px'},h('span',{class:'label'},'Steps '),x.step_ids.map(s=>[h('code',{class:e.runnable.includes(s)?'':'',style:e.runnable.includes(s)?'color:var(--run);font-weight:700':''},s),' '])),),
  h('div',{class:'card'},field('Search process',e.search_process,'cent'),h('div',{style:'height:6px'}),field('Feedback response',e.feedback_response),h('div',{style:'height:6px'}),field('Exit',e.exit),h('div',{style:'height:6px'}),field('Relied on unseen',e.unseen),h('div',{style:'height:6px'}),field('Evidence',e.evidence)),
  h('h3',{},`Extracted items (${e.items.length})`),e.items.map(i=>itemBox(i,true)));
  return n}
function consensus(c){return h('div',{},h('div',{class:'label'},'Prior situation'),h('ul',{},c.prior_situation.map(s=>h('li',{},s))),
  (c.changes||[]).map((ch,i)=>h('div',{class:'card'},h('div',{class:'label'},'Change '+(i+1)),field('Problem',ch.problem),field('Lever',ch.lever),field('Value',ch.value),field('Decision',ch.decision),field('Reasoning',ch.reasoning),field('Why this lever',ch.why_lever,'cent'),field('Why this value',ch.why_value,'acc'))),
  h('h3',{},'Rationale items'),(c.rationales||[]).map((r,i)=>{const id=null;return itemBox({...r,id:`#${i+1}`},true)}),field('Evidence',c.evidence),h('div',{class:'muted'},'confidence '+c.confidence))}
function dStep(s){
  return h('div',{},h('div',{class:'card'},h('div',{class:'big'},s.goal),h('div',{class:'kv'},h('code',{},s.id),h('span',{},s.comp),h('span',{},`${s.n_samples} samples, agreement ${s.agreement}, plausible ${s.plausible}`)),
    s.disagreements&&h('div',{class:'muted'},'disagreements: '+s.disagreements),
    D.eps.filter(e=>e.ep.step_ids.includes(s.id)).map(e=>h('div',{},'also covered by episode ',lnk('eps',e.id)))),
    consensus(s.consensus))}
function dChunk(c){const n=h('div',{},h('div',{class:'card'},h('div',{class:'label'},'Goal'),h('div',{class:'big'},c.goal),h('div',{class:'muted'},c.overview),h('div',{class:'meta'},`${c.ids.length} items: `,c.ids.map(i=>[lnk('steps',i.split('#')[0],i),' ']))));
  c.lever_contexts.forEach(lc=>{n.append(field('Lever context',lc.lever_context,'cent'));
    (lc.levers||[]).forEach(lv=>{n.append(h('div',{class:'indent'},h('div',{class:'big'},lv.lever),h('div',{class:'muted'},lv.selected_when),
      (lv.actions||[]).map(ac=>h('div',{class:'indent'},field('Action context',ac.action_context,'acc'),field('Action',ac.action),field('Nuance',ac.nuance),h('div',{class:'meta'},ac.sources.map(i=>[lnk('steps',i.split('#')[0],i),' '])))) ))})});
  if(c.unplaced&&c.unplaced.length)n.append(h('div',{class:'muted'},'unplaced: '+c.unplaced.join(', ')));
  return n}
setMode('rules');
</script></body></html>
"""


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--runnable-csv", default=str(HERE.parents[1] / "tacit-eval-pipeline" / "triage" / "runnable_cases.csv"))
    ap.add_argument("--out", default=str(RES / "knowledge_viewer.html"))
    a = ap.parse_args()
    d = clean(load(a.runnable_csv))
    blob = json.dumps(d, ensure_ascii=False, separators=(",", ":"), allow_nan=False).replace("</", "<\\/")
    Path(a.out).write_text(PAGE.replace("__DATA__", blob), encoding="utf-8")
    print(f"{len(d['rules'])} rules, {len(d['eps'])} episodes, {len(d['steps'])} steps, {len(d['chunks'])} step clusters, "
          f"{d['n_run_pairs']} runnable pairs -> {a.out} ({Path(a.out).stat().st_size / 1e6:.1f} MB)")
