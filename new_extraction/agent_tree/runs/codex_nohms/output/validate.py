"""Validate the tree against the original episode items; run from the project directory."""
import json
from collections import Counter
from pathlib import Path

base = Path(__file__).resolve().parent
with (base.parent / 'episode_items.jsonl').open() as f:
    expected = [f"{row['ep_id']}#{k}" for line in f
                for row in [json.loads(line)] for k in range(1, len(row['items']) + 1)]
assert len(expected) == len(set(expected)), 'Duplicate source item IDs'
tree = json.loads((base / 'tree.json').read_text())
desiderata = json.loads((base / 'desiderata.json').read_text())['nodes']
seen_nodes, placed, decisions = {}, [], set()
leaves = checks = 0

def visit(node, expected_id):
    global leaves, checks
    nid = node['id']
    assert nid == expected_id, (nid, expected_id)
    assert nid not in seen_nodes, f'Duplicate node: {nid}'
    seen_nodes[nid] = node
    assert node['name'] and node['description'], nid
    assert node['source'] in ('data', 'prior'), nid
    children = node['children']
    if children:
        decisions.add(nid)
        assert node.get('decision') and 'items' not in node, nid
        assert nid in desiderata, f'Missing desiderata: {nid}'
        child_ids = {c['id'] for c in children}
        groups = desiderata[nid]['groups']
        assert groups and all(g['checks'] for g in groups), nid
        supported = set()
        for group in groups:
            for check in group['checks']:
                checks += 1
                assert check['check'] and check['how'] and check['pushes'], nid
                assert set(check['pushes']) <= child_ids, (nid, check)
                assert all(isinstance(w, (int, float)) and -1 <= w <= 1
                           for w in check['pushes'].values()), (nid, check)
                supported.update(k for k, w in check['pushes'].items() if w > 0)
        assert supported == child_ids, f'Unrouted options: {nid}'
        for i, child in enumerate(children, 1):
            assert 'unassigned' not in child, child['id']
            visit(child, f'{nid}.{i}')
    else:
        leaves += 1
        assert 'decision' not in node and isinstance(node['items'], list), nid
        assert node['items'] or node['source'] == 'prior', nid
        placed.extend(node['items'])
        for evidence in node.get('evidence', []):
            assert evidence['item'] in node['items'], (nid, evidence)

visit(tree, 'T')
assert set(desiderata) == decisions, 'Desiderata contain missing or nondecision nodes'
unassigned = tree['unassigned']
assert all(u['reason'] and '\n' not in u['reason'] for u in unassigned)
actual = Counter(placed + [u['item'] for u in unassigned])
assert actual == Counter(expected), {
    'missing': sorted(set(expected) - set(actual)),
    'unknown': sorted(set(actual) - set(expected)),
    'duplicates': {k: v for k, v in actual.items() if v > 1},
}
print(f'items placed: {len(placed)}')
print(f'unassigned: {len(unassigned)}')
print(f'leaves: {leaves}')
print(f'decision nodes: {len(decisions)}')
print(f'checks: {checks}')
