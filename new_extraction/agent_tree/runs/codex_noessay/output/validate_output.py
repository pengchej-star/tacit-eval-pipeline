"""Validate item coverage, tree structure, and actionable check references."""
import collections
import json
import math
from pathlib import Path

base = Path(__file__).resolve().parent.parent
out = base / 'output'
expected = []
for line in (base / 'episode_items.jsonl').open():
    episode = json.loads(line)
    expected.extend(f"{episode['ep_id']}#{k}" for k in range(1, len(episode['items']) + 1))
assert len(expected) == len(set(expected)), 'Duplicate input item IDs'
tree = json.loads((out / 'tree.json').read_text())
desiderata = json.loads((out / 'desiderata.json').read_text())['nodes']
seen_nodes = set()
placed = []
decisions = set()
leaf_count = 0
check_count = 0

def visit(node, required_id):
    global leaf_count, check_count
    node_id = node['id']
    assert node_id == required_id, (node_id, required_id)
    assert node_id not in seen_nodes, ('Duplicate node ID', node_id)
    seen_nodes.add(node_id)
    for field in ('name', 'description'):
        assert isinstance(node.get(field), str) and node[field].strip(), (node_id, field)
    assert node['source'] in ('data', 'prior'), node_id
    assert isinstance(node['children'], list), node_id
    if node_id != 'T':
        assert 'unassigned' not in node, node_id
    children = node['children']
    if children:
        decisions.add(node_id)
        assert len(children) >= 2, ('Unary decision', node_id)
        assert isinstance(node.get('decision'), str) and node['decision'].strip(), node_id
        assert 'items' not in node, ('Items on internal node', node_id)
        assert node_id in desiderata, ('Missing desiderata', node_id)
        child_ids = {c['id'] for c in children}
        positively_supported = set()
        groups = desiderata[node_id]['groups']
        assert groups, node_id
        for group in groups:
            assert isinstance(group['under'], str) and group['under'].strip(), node_id
            assert group['checks'], node_id
            for check in group['checks']:
                check_count += 1
                for field in ('check', 'how'):
                    assert isinstance(check.get(field), str) and check[field].strip(), (node_id, field)
                assert not check['check'].strip().endswith('?'), ('Check must be a statement', node_id)
                pushes = check['pushes']
                assert isinstance(pushes, dict) and pushes, node_id
                assert set(pushes) <= child_ids, ('Push outside children', node_id, pushes)
                for child, weight in pushes.items():
                    assert type(weight) in (int, float) and math.isfinite(weight), (node_id, weight)
                    assert -1 <= weight <= 1 and weight != 0, (node_id, weight)
                    if weight > 0:
                        positively_supported.add(child)
        assert positively_supported == child_ids, ('Child lacks positive routing check', node_id, child_ids - positively_supported)
        for i, child in enumerate(children, 1):
            visit(child, f'{node_id}.{i}')
    else:
        leaf_count += 1
        assert 'decision' not in node, node_id
        assert isinstance(node.get('items'), list), node_id
        assert node['items'] or node['source'] == 'prior', ('Empty data leaf', node_id)
        placed.extend(node['items'])

visit(tree, 'T')
assert set(desiderata) == decisions, ('Missing/orphan desiderata', set(desiderata) ^ decisions)
unassigned = tree['unassigned']
for entry in unassigned:
    assert isinstance(entry['reason'], str) and entry['reason'].strip(), entry
counts = collections.Counter(placed + [entry['item'] for entry in unassigned])
assert set(counts) == set(expected), {'missing': sorted(set(expected) - set(counts)), 'unknown': sorted(set(counts) - set(expected))}
assert all(count == 1 for count in counts.values()), {item: count for item, count in counts.items() if count != 1}
assert (out / 'notes.md').is_file(), 'Missing notes'
print(f'Items placed: {len(placed)}')
print(f'Items unassigned: {len(unassigned)}')
print(f'Leaves: {leaf_count}')
print(f'Decision nodes: {len(decisions)}')
print(f'Checks: {check_count}')
print(f'Coverage: {len(counts)}/{len(expected)}; all validation checks passed')
