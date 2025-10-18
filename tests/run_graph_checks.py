#!/usr/bin/env python3
"""Simple runner to check sample graphs in graphs/ without pytest."""
import os
import glob
import sys

from graph_analyzer.utils.graph_parser import GraphParser
from graph_analyzer.models.graph import Graph
from graph_analyzer.analyzers.graph_properties_analyzer import GraphPropertiesAnalyzer


GRAPHS_DIR = os.path.join(os.path.dirname(__file__), '..', 'graphs')


def load_graph(path):
    nodes, edges = GraphParser.parse_file(path)
    g = Graph()
    g.load_from_data(nodes, edges)
    return g


def check_all():
    pattern = os.path.join(GRAPHS_DIR, '*')
    files = [p for p in glob.glob(pattern) if os.path.isfile(p)]
    if not files:
        print('No graph files found in', GRAPHS_DIR)
        return 2

    failures = []
    for f in sorted(files):
        name = os.path.basename(f)
        try:
            g = load_graph(f)
            ana = GraphPropertiesAnalyzer(g)
            props = ana.get_basic_properties()
        except Exception as e:
            failures.append((name, 'exception', str(e)))
            continue

        # File-specific expectations
        if name == 'tree.tg':
            if not ana.is_tree():
                failures.append((name, 'is_tree', props))
        if name == 'noEdges.txt':
            if props['component_count'] != props['node_count']:
                failures.append((name, 'components_vs_nodes', props))
        if name == 'twoCycles.txt':
            if not ana.has_cycles():
                failures.append((name, 'has_cycles', props))

        print(f'[OK] {name}: nodes={props["node_count"]} edges={props["edge_count"]} directed={props["is_directed"]}')

    print('\nSummary:')
    if not failures:
        print('All checks passed')
        return 0
    else:
        print(f'{len(failures)} failure(s)')
        for f in failures:
            print('-', f)
        return 1


if __name__ == '__main__':
    rc = check_all()
    sys.exit(rc)
