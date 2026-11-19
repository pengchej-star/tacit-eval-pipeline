"""Validate the generated tree against the original episode items."""
import collections
import json
import math
from pathlib import Path

base = Path(__file__).resolve().parent.parent
expected = []
for line in (base / 'episode_items.jsonl').read_text().splitlines():
    episode = json.loads(line)
    expected.extend(f"{episode['ep_id']}#{k}" for k in range(1, len(episode['items']) + 1))
assert len(expected) == len(set(expected)), 'Duplicate item IDs in input'
tree = json.loads((base / 'output/tree.json').read_text())
desiderata = json.loads((base / 'output/desiderata.json').read_text())
placed, unassigned, ids, decisions = [], [], set(), set()
stats = collections.Counter()

def visit(node, path):
    assert node['id'] == path, (node['id'], path)
    assert path not in ids, f'Duplicate node: {path}'
    ids.add(path)
    for field in ('name', 'description'):
        assert isinstance(node.get(field), str) and node[field].strip(), (path, field)
    assert node.get('source') in ('data', 'prior'), (path, 'source')
    assert isinstance(node['children'], list)
    assert path == 'T' or 'unassigned' not in node
    children = node['children']
    if children:
        stats['decision_nodes'] += 1
        decisions.add(path)
        assert len(children) >= 2, f'Unary routing node: {path}'
        assert node.get('decision', '').strip(), f'Missing question: {path}'
        assert 'items' not in node, f'Items on a decision: {path}'
        assert path in desiderata['nodes'], f'Missing desiderata: {path}'
        valid_children = {f'{path}.{i}' for i in range(1, len(children) + 1)}
        mentioned = set()
        groups = desiderata['nodes'][path]['groups']
        assert groups, f'Empty desiderata: {path}'
        for group in groups:
            assert group['under'].strip() and group['checks']
            for check in group['checks']:
                stats['checks'] += 1
                assert check['check'].strip() and check['how'].strip()
                assert not check['check'].rstrip().endswith('?'), f'Check is a question: {path}'
                assert check['pushes'], f'Empty pushes: {path}'
                for child, weight in check['pushes'].items():
                    assert child in valid_children, (path, 'non-child push', child)
                    assert isinstance(weight, (int, float)) and not isinstance(weight, bool)
                    assert math.isfinite(weight) and -1 <= weight <= 1, (path, child, weight)
                    assert weight != 0, (path, 'zero push', child)
                    mentioned.add(child)
        assert mentioned == valid_children, (path, 'unaddressed options', valid_children - mentioned)
        for i, child in enumerate(children, 1):
            visit(child, f'{path}.{i}')
    else:
        stats['leaves'] += 1
        assert 'decision' not in node, f'Question on leaf: {path}'
        assert isinstance(node.get('items'), list)
        assert node['items'] or node['source'] == 'prior', f'Empty data leaf: {path}'
        placed.extend(node['items'])

visit(tree, 'T')
for item in tree.get('unassigned', []):
    assert item['reason'].strip()
    unassigned.append(item['item'])
actual = collections.Counter(placed + unassigned)
assert set(actual) == set(expected), {'missing': set(expected) - set(actual), 'unknown': set(actual) - set(expected)}
assert all(n == 1 for n in actual.values()), {k: v for k, v in actual.items() if v != 1}
assert set(desiderata['nodes']) == decisions, 'Extraneous or absent decision desiderata'
assert (base / 'output/notes.md').is_file()
print(f"Items placed: {len(placed)}; unassigned: {len(unassigned)}; total accounted for: {len(actual)}")
print(f"Leaves: {stats['leaves']}; decision nodes: {stats['decision_nodes']}; checks: {stats['checks']}")
print('PASS: valid JSON, exact item coverage, node nesting, and desiderata references.')
