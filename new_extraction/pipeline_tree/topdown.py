"""Step 1 (top-down): the LLM writes the tree of 'what can one change to improve a model' from parametric knowledge only."""
from common import CFG, OUT, ROOT, ask, fill, jdump, jload
from prompts import TOPDOWN

def assign_ids(node, nid="T", depth=0):
    node["id"], node["depth"], node["source"] = nid, depth, "top_down"
    for i, c in enumerate(node.get("children") or [], 1):
        assign_ids(c, f"{nid}.{i}", depth + 1)
    return node


def run():
    p = OUT / "1_topdown.json"
    shared = ROOT / CFG["paths"]["skeleton"]   # the prompt carries no competition information, so one skeleton serves all
    if p.exists():
        return
    if shared.exists():
        jdump(jload(shared), p)
        print("top-down tree: reused", shared.name)
        return
    d = CFG["topdown"]["depth"]
    tree = ask(fill(TOPDOWN, depth=d), "Write the tree.", max_tokens=12000, temperature=0.4)
    assert "children" in tree, tree
    assign_ids(tree)
    jdump(tree, p)
    jdump(tree, shared)
    n = [0]
    def walk(x):
        n[0] += 1
        for c in x.get("children") or []:
            walk(c)
    walk(tree)
    print(f"top-down tree: {n[0]} nodes")


if __name__ == "__main__":
    run()
