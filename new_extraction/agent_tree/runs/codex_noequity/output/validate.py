"""Validate the tree against the source JSONL; run with python output/validate.py."""
import collections
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent

def main():
    # Parse every delivered JSON file, not just the two expected ones.
    for path in OUT.glob('*.json'):
        json.loads(path.read_text())
    tree = json.loads((OUT / 'tree.json').read_text())
    desiderata = json.loads((OUT / 'desiderata.json').read_text())['nodes']
    expected = []
    for line in (ROOT / 'episode_items.jsonl').read_text().splitlines():
        row = json.loads(line)
        expected.extend(f"{row['ep_id']}#{k}" for k in range(1, len(row['items']) + 1))
    assert len(expected) == len(set(expected)), 'Duplicate item IDs in input'
    seen_nodes, assigned = {}, []
    leaf_count = decision_count = check_count = 0

    def walk(node, ident):
        nonlocal leaf_count, decision_count, check_count
        assert node['id'] == ident, f"Nesting mismatch: {node['id']} != {ident}"
        assert ident not in seen_nodes, f'Duplicate node ID: {ident}'
        seen_nodes[ident] = node
        for field in ['name', 'description']:
            assert isinstance(node.get(field), str) and node[field].strip(), (ident, field)
        assert node.get('source') in ['data', 'prior'], (ident, 'source')
        children = node['children']
        assert isinstance(children, list), (ident, 'children')
        if children:
            decision_count += 1
            assert len(children) >= 2, f'Unary decision: {ident}'
            assert isinstance(node.get('decision'), str) and node['decision'].strip(), ident
            assert 'items' not in node, f'Items on decision: {ident}'
            assert ident in desiderata, f'Missing desiderata: {ident}'
            child_ids = {c['id'] for c in children}
            groups = desiderata[ident]['groups']
            assert groups, f'Empty desiderata: {ident}'
            covered = set()
            for group in groups:
                assert group['under'].strip() and group['checks'], ident
                for check in group['checks']:
                    check_count += 1
                    assert check['check'].strip() and check['how'].strip(), ident
                    assert '?' not in check['check'], f'Check is a question: {ident}'
                    assert check['pushes'], f'Empty pushes: {ident}'
                    for target, weight in check['pushes'].items():
                        assert target in child_ids, f'{ident} pushes non-child {target}'
                        assert type(weight) in [float, int] and -1 <= weight <= 1, (ident, weight)
                        assert weight != 0, f'Zero-effect push: {ident}'
                        covered.add(target)
            assert covered == child_ids, f'Options with no checks: {ident}: {child_ids-covered}'
            for j, child in enumerate(children, 1):
                walk(child, f'{ident}.{j}')
        else:
            leaf_count += 1
            assert 'decision' not in node, f'Question on leaf: {ident}'
            assert isinstance(node['items'], list), ident
            if node['source'] == 'data':
                assert node['items'], f'Empty data leaf: {ident}'
            assigned.extend(node['items'])
        if ident != 'T':
            assert 'unassigned' not in node, f'Nested unassigned: {ident}'

    walk(tree, 'T')
    assert set(desiderata) == {k for k,v in seen_nodes.items() if v['children']}, 'Extra or missing desiderata nodes'
    unassigned = tree['unassigned']
    for entry in unassigned:
        assert entry['reason'].strip() and '\n' not in entry['reason'], entry
    observed = assigned + [u['item'] for u in unassigned]
    counts = collections.Counter(observed)
    duplicates = [k for k,v in counts.items() if v != 1]
    missing, unknown = set(expected)-set(observed), set(observed)-set(expected)
    assert not duplicates, f'Duplicate assignments: {duplicates}'
    assert not missing, f'Missing items: {missing}'
    assert not unknown, f'Unknown items: {unknown}'
    assert tree['decision'] == 'what can I change to improve my solution?'
    print(f'Items placed: {len(assigned)}')
    print(f'Unassigned: {len(unassigned)}')
    print(f'Leaves: {leaf_count}')
    print(f'Decision nodes: {decision_count}')
    print(f'Checks: {check_count}')
    print('Validation: PASS')

if __name__ == '__main__':
    main()
