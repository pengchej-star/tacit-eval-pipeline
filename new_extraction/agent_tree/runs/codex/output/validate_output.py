"""Validate the decision tree against the source items; run from any directory."""
import json
from collections import Counter
from pathlib import Path

out = Path(__file__).resolve().parent

def read_json(path):
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            assert key not in result, f'Duplicate JSON key: {key}'
            result[key] = value
        return result
    return json.loads(path.read_text(), object_pairs_hook=unique_keys)

expected = []
with (out.parent / 'episode_items.jsonl').open() as source:
    for line in source:
        episode = json.loads(line)
        expected.extend(f"{episode['ep_id']}#{k}" for k in range(1, len(episode['items']) + 1))
assert len(expected) == len(set(expected)), 'Duplicate source item IDs'
tree = read_json(out / 'tree.json')
desiderata = read_json(out / 'desiderata.json')
assert tree['decision'] == 'what can I change to improve my solution?'
nodes, decisions, placed = {}, {}, []
leaf_count = 0

def walk(node, identifier):
    global leaf_count
    assert node['id'] == identifier, f'Inconsistent nesting: {node["id"]}, expected {identifier}'
    assert identifier not in nodes, f'Duplicate node ID: {identifier}'
    nodes[identifier] = node
    for field in ('name', 'description'):
        assert isinstance(node[field], str) and node[field].strip(), (identifier, field)
    assert node['source'] in ('data', 'prior'), identifier
    assert isinstance(node['children'], list), identifier
    if identifier != 'T':
        assert 'unassigned' not in node, identifier
    if node['children']:
        assert isinstance(node['decision'], str) and node['decision'].strip(), identifier
        assert 'items' not in node, f'Items on decision {identifier}'
        assert len(node['children']) >= 2, f'Unnecessary single-child decision {identifier}'
        decisions[identifier] = node
        for position, child in enumerate(node['children'], 1):
            walk(child, f'{identifier}.{position}')
    else:
        assert 'decision' not in node, f'Decision on leaf {identifier}'
        assert isinstance(node['items'], list), identifier
        assert node['items'] or node['source'] == 'prior', f'Empty data leaf {identifier}'
        placed.extend(node['items'])
        leaf_count += 1

walk(tree, 'T')
unassigned = tree['unassigned']
for entry in unassigned:
    assert isinstance(entry['reason'], str) and entry['reason'].strip()
    assert '\n' not in entry['reason'], 'Unassigned reason must be one line'
all_placements = Counter(placed + [entry['item'] for entry in unassigned])
assert set(all_placements) == set(expected), {
    'missing': sorted(set(expected) - set(all_placements)),
    'unknown': sorted(set(all_placements) - set(expected)),
}
assert all(count == 1 for count in all_placements.values()), {
    'duplicates': [item for item, count in all_placements.items() if count != 1]
}
assert set(desiderata['nodes']) == set(decisions), 'Decision/desiderata coverage mismatch'
check_count = 0
for identifier, decision in decisions.items():
    children = {child['id'] for child in decision['children']}
    supported = set()
    groups = desiderata['nodes'][identifier]['groups']
    assert groups, f'No desiderata groups for {identifier}'
    for group in groups:
        assert group['under'].strip() and group['checks'], identifier
        for check in group['checks']:
            assert check['check'].strip() and check['how'].strip(), identifier
            assert not check['check'].rstrip().endswith('?'), 'Use statements, not questions'
            assert check['pushes'], f'Check with no effect: {identifier}'
            for child, weight in check['pushes'].items():
                assert child in children, f'{identifier} pushes nonchild {child}'
                assert type(weight) in (float, int) and -1 <= weight <= 1 and weight != 0
                if weight > 0:
                    supported.add(child)
            check_count += 1
    assert supported == children, f'Options without positive selection evidence: {children - supported}'
print(f'Items placed: {len(placed)}')
print(f'Unassigned: {len(unassigned)}')
print(f'Leaves: {leaf_count}')
print(f'Decision nodes: {len(decisions)}')
print(f'Checks: {check_count}')
