"""Validate tree structure, item accounting, and decision checks using only local files."""
import collections
import json
import math
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT = BASE.parent / 'episode_items.jsonl'
expected = []
for line in INPUT.read_text().splitlines():
    episode = json.loads(line)
    expected.extend(f"{episode['ep_id']}#{k}" for k in range(1, len(episode['items']) + 1))
assert len(expected) == len(set(expected)), 'Duplicate IDs in input'
tree = json.loads((BASE / 'tree.json').read_text())
desiderata = json.loads((BASE / 'desiderata.json').read_text())
seen, placed, leaves, decisions = {}, [], [], []

def visit(node, expected_id):
    assert node['id'] == expected_id, ('Wrong nesting ID', node['id'], expected_id)
    assert node['id'] not in seen, ('Duplicate node ID', node['id'])
    seen[node['id']] = node
    for field in ('name', 'description'):
        assert isinstance(node.get(field), str) and node[field].strip(), (expected_id, field)
    assert node.get('source') in ('data', 'prior'), (expected_id, 'source')
    assert isinstance(node.get('children'), list), (expected_id, 'children')
    if node['children']:
        assert len(node['children']) >= 2, ('Unary decision', expected_id)
        assert isinstance(node.get('decision'), str) and node['decision'].strip()
        assert 'items' not in node, ('Items on decision', expected_id)
        decisions.append(node)
        for k, child in enumerate(node['children'], 1):
            visit(child, f'{expected_id}.{k}')
    else:
        assert 'decision' not in node, ('Decision on leaf', expected_id)
        assert isinstance(node.get('items'), list), ('Missing leaf items', expected_id)
        assert node['items'] or node['source'] == 'prior', ('Empty data leaf', expected_id)
        placed.extend(node['items'])
        leaves.append(node)
    if expected_id != 'T':
        assert 'unassigned' not in node, ('Nested unassigned', expected_id)

visit(tree, 'T')
assert tree['decision'] == 'what can I change to improve my solution?'
unassigned = tree['unassigned']
for entry in unassigned:
    assert isinstance(entry['reason'], str) and entry['reason'].strip()
    assert '\n' not in entry['reason'], ('Multiline reason', entry['item'])
accounted = collections.Counter(placed + [entry['item'] for entry in unassigned])
assert set(accounted) == set(expected), {
    'missing': sorted(set(expected) - set(accounted)),
    'unknown': sorted(set(accounted) - set(expected))}
assert all(n == 1 for n in accounted.values()), {
    'duplicates': {key: n for key, n in accounted.items() if n != 1}}
assert set(desiderata['nodes']) == {node['id'] for node in decisions}, 'Desiderata/node mismatch'
checks = 0
for node in decisions:
    entry = desiderata['nodes'][node['id']]
    children = {child['id'] for child in node['children']}
    assert entry['groups'], ('Empty desiderata', node['id'])
    supported = set()
    for group in entry['groups']:
        assert group['under'] and group['checks']
        for check in group['checks']:
            checks += 1
            assert check['check'].strip() and check['how'].strip()
            assert not check['check'].strip().endswith('?'), ('Question instead of statement', check)
            assert check['pushes'], ('Empty pushes', node['id'])
            for child_id, weight in check['pushes'].items():
                assert child_id in children, ('Not an immediate child', node['id'], child_id)
                assert isinstance(weight, (float, int)) and not isinstance(weight, bool)
                assert math.isfinite(weight) and -1 <= weight <= 1 and weight != 0
                if weight > 0:
                    supported.add(child_id)
    assert supported == children, ('Option lacks a positive selection check', node['id'], children - supported)
print(f'Items placed: {len(placed)}')
print(f'Unassigned: {len(unassigned)}')
print(f'Leaves: {len(leaves)}')
print(f'Decision nodes: {len(decisions)}')
print(f'Checks: {checks}')
