import os
import sys

from .models import Graph
from .utils import GraphParser
from .analyzers import GraphPropertiesAnalyzer, PathAnalyzer, MatrixAnalyzer


def load_graph(input_file):
    """Načte graf ze souboru a vrátí objekt Graph."""
    try:
        nodes_dict, edges_list = GraphParser.parse_file(input_file)
        graph = Graph()
        graph.load_from_data(nodes_dict, edges_list)
        return graph
    except FileNotFoundError:
        raise
    except Exception:
        raise


def print_basic_info(graph, quiet=False):
    """Vytiskne základní informace o grafu."""
    if not quiet:
        print("="*60)
        print("ZÁKLADNÍ INFORMACE O GRAFU")
        print("="*60)

    print(f"Počet uzlů:_________{graph.get_node_count()}")
    print(f"Počet hran:_________{graph.get_edge_count()}")


def analyze_properties(graph, quiet=False):
    """Analyzuje vlastnosti grafu a vytiskne je."""
    analyzer = GraphPropertiesAnalyzer(graph)
    properties = analyzer.get_basic_properties()

    def _fmt_bool(val):
        """Vrací 'Ano'/'Ne' (či barevnou variantu) pro boolean hodnoty."""
        # If not a TTY, return plain Czech Yes/No
        if not sys.stdout.isatty():
            return 'Ano' if val else 'Ne'
        # Use ANSI colors: green for True, red for False
        if val:
            return f"\x1b[32mAno\x1b[0m"
        else:
            return f"\x1b[31mNe\x1b[0m"

    if not quiet:
        print("\n" + "="*60)
        print("VLASTNOSTI GRAFU")
        print("="*60)

    print(f"Orientovaný:________{_fmt_bool(properties['is_directed'])}")
    print(f"Ohodnocený:_________{_fmt_bool(properties['is_weighted'])}")
    print(f"Prostý:_____________{_fmt_bool(properties['is_simple'])}")
    print(f"Souvislý:___________{_fmt_bool(properties['is_connected'])}")
    print(f"Úplný:______________{_fmt_bool(properties['is_complete'])}")
    print(f"Regulární:__________{_fmt_bool(properties['is_regular'])}")
    print(f"Bipartitní:_________{_fmt_bool(properties['is_bipartite'])}")
    print(f"Strom:______________{_fmt_bool(properties['is_tree'])}")
    print(f"Les:________________{_fmt_bool(properties['is_forest'])}")
    print(f"Obsahuje smyčky:____{_fmt_bool(properties['has_loops'])}")
    print(f"Obsahuje cykly:_____{_fmt_bool(properties['has_cycles'])}")
    print(f"Rovinný (heur.):____{_fmt_bool(analyzer.is_planar_graph())}")
    print(f"Počet komponent:____{properties['component_count']}")


def analyze_node(graph, node_id, analysis_type, quiet=False):
    """Analyzuje konkrétní uzel."""
    if not graph.has_node(node_id):
        print(f"Chyba: Uzel '{node_id}' neexistuje v grafu.", file=sys.stderr)
        return

    if not quiet:
        print(f"\n{'='*60}")
        print(f"ANALÝZA UZLU '{node_id}'")
        print("="*60)

    if analysis_type == 'neighbors':
        neighbors = graph.get_neighbors(node_id)
        print(f"Sousedé uzlu '{node_id}': {neighbors}")

    elif analysis_type == 'degree':
        degree_info = graph.get_node_degree(node_id)
        if graph.is_directed:
            print(f"Vstupní stupeň:     {degree_info['in_degree']}")
            print(f"Výstupní stupeň:    {degree_info['out_degree']}")
            print(f"Celkový stupeň:     {degree_info['total_degree']}")
        else:
            print(f"Stupeň uzlu: {degree_info['total_degree']}")
        print(f"Izolovaný uzel: {graph.is_isolated_node(node_id)}")

    elif analysis_type == 'all':
        node = graph.get_node(node_id)
        print(f"\n{'-'*40}")
        print(f"VŠECHNY VLASTNOSTI UZLU '{node_id}'")
        print(f"{'-'*40}")
        print(f"Identifier: {node.identifier}")
        print(f"Value: {node.value}")
        neighbors = graph.get_neighbors(node_id)
        print(f"Sousedé: {neighbors}")

        # Use analyzer helpers so undirected graphs return neighbors for successors/predecessors
        from .analyzers import GraphPropertiesAnalyzer
        analyzer = GraphPropertiesAnalyzer(graph)
        print(f"Následníci: {analyzer.get_successors(node_id)}")
        print(f"Předchůdci: {analyzer.get_predecessors(node_id)}")

        # Use analyzer helpers to get in/out/total degrees
        out_deg = analyzer.out_degree(node_id)
        in_deg = analyzer.in_degree(node_id)
        total_deg = analyzer.degree(node_id)
        print(f"Vstupní stupeň: {in_deg}, Výstupní stupeň: {out_deg}, Celkový: {total_deg}")

        # incident edges
        inc_edges = analyzer.incident_edges(node_id)
        print(f"Incidentní hrany (u -> v, směr, váha):")
        for e in inc_edges:
            print(f"  {e.u.identifier} {e.direction} {e.v.identifier} (weight={e.weight})")
        print(f"Izolovaný: {graph.is_isolated_node(node_id)}")

    elif analysis_type == 'successors':
        successors = graph.get_successors(node_id)
        print(f"Následníci uzlu '{node_id}': {successors}")

    elif analysis_type == 'predecessors':
        predecessors = graph.get_predecessors(node_id)
        print(f"Předchůdci uzlu '{node_id}': {predecessors}")


def analyze_paths(graph, args, quiet=False):
    """Analyzuje cesty v grafu."""
    path_analyzer = PathAnalyzer(graph)

    if args.path:
        start, end = args.path
        if not quiet:
            print(f"\n{'='*60}")
            print(f"NEJKRATŠÍ CESTA: {start} → {end}")
            print("="*60)

        path = path_analyzer.find_shortest_path(start, end)
        if path:
            print(f"Nejkratší cesta: {' → '.join(path)}")
            if graph.is_weighted:
                total_weight = 0
                for u, v in zip(path[:-1], path[1:]):
                    for edge in graph.adj[u]:
                        if edge.v.identifier == v:
                            total_weight += edge.weight
                            break
                print(f"Délka cesty: {total_weight}")
            else:
                print(f"Délka cesty: {len(path) - 1}")
        else:
            print("Cesta neexistuje")

    if args.all_paths:
        start, end = args.all_paths
        if not quiet:
            print(f"\n{'='*60}")
            print(f"VŠECHNY CESTY: {start} → {end}")
            print("="*60)

        paths = path_analyzer.find_all_paths(start, end, max_length=10)
        if paths:
            print(f"Nalezeno {len(paths)} cest:")
            for i, path in enumerate(paths[:args.max_paths], 1):
                if graph.is_weighted:
                    total_weight = 0
                    for u, v in zip(path[:-1], path[1:]):
                        for edge in graph.adj[u]:
                            if edge.v.identifier == v:
                                total_weight += edge.weight
                                break
                    print(f"  {i}. {' → '.join(path)} (délka: {total_weight})")
                else:
                    print(f"  {i}. {' → '.join(path)} (délka: {len(path) - 1})")
            if len(paths) > args.max_paths:
                print(f"  ... a dalších {len(paths) - args.max_paths} cest")
        else:
            print("Žádné cesty nebyly nalezeny")

    if args.distances:
        node_id = args.distances
        if not quiet:
            print(f"\n{'='*60}")
            print(f"VZDÁLENOSTI OD UZLU '{node_id}'")
            print("="*60)

        distances = path_analyzer.get_shortest_distances(node_id)
        for target_id, distance in sorted(distances.items()):
            if target_id != node_id:
                if distance == float('inf'):
                    print(f"  {node_id} → {target_id}: nedostupný")
                else:
                    print(f"  {node_id} → {target_id}: {distance}")

    if args.diameter:
        if not quiet:
            print(f"\n{'='*60}")
            print("PRŮMĚR GRAFU")
            print("="*60)

        diameter = path_analyzer.get_graph_diameter()
        if diameter == float('inf'):
            print("Průměr: nekonečno (graf není souvislý)")
        else:
            print(f"Průměr grafu: {diameter}")

    if args.radius:
        if not quiet:
            print(f"\n{'='*60}")
            print("POLOMĚR GRAFU")
            print("="*60)

        radius = path_analyzer.get_graph_radius()
        if radius == float('inf'):
            print("Poloměr: nekonečno (graf není souvislý)")
        else:
            print(f"Poloměr grafu: {radius}")

    if args.center:
        if not quiet:
            print(f"\n{'='*60}")
            print("CENTRÁLNÍ UZLY")
            print("="*60)

        center_nodes = path_analyzer.find_center_nodes()
        if center_nodes:
            print(f"Centrální uzly: {center_nodes}")
        else:
            print("Žádné centrální uzly (graf není souvislý)")


def analyze_matrices(graph, args, quiet=False):
    """Analyzuje maticové reprezentace grafu."""
    matrix_analyzer = MatrixAnalyzer(graph)

    if not quiet:
        print(f"\n{'='*60}")
        print("MATICOVÉ REPREZENTACE")
        print("="*60)

    show_any_specific = any([
        getattr(sys, 'argv', None) and '--adjacency' in sys.argv,
        getattr(sys, 'argv', None) and '--incidence' in sys.argv,
        getattr(sys, 'argv', None) and '--weight' in sys.argv,
        getattr(sys, 'argv', None) and '--adj-power' in sys.argv,
    ])

    export_dir = None
    if getattr(sys, 'argv', None) and '--export-csv' in sys.argv:
        try:
            export_dir = sys.argv[sys.argv.index('--export-csv') + 1]
        except Exception:
            export_dir = None

    # Interaktivní režim s maticemi
    if getattr(args, 'matrix_ops', False):
        print("\n" + "="*60)
        print("INTERAKTIVNÍ OPERACE S MATICEMI")
        print("="*60)
        print("Vyberte matici pro práci:")
        print("1. Matice sousednosti")
        print("2. Matice incidence")
        if graph.is_weighted:
            print("3. Matice vah")
        print("0. Zpět")
        
        try:
            choice = input("\nVaše volba: ").strip()
            if choice == '1':
                matrix, nodes = matrix_analyzer.get_adjacency_matrix()
                if matrix:
                    matrix_analyzer.print_adjacency_matrix()
                    matrix_analyzer.interactive_matrix_operations(matrix, nodes, "Matice sousednosti")
                else:
                    print("Matice sousednosti je prázdná")
            elif choice == '2':
                matrix, nodes, edges = matrix_analyzer.get_incidence_matrix()
                if matrix:
                    matrix_analyzer.print_incidence_matrix()
                    matrix_analyzer.interactive_matrix_operations(matrix, nodes, "Matice incidence")
                else:
                    print("Matice incidence je prázdná")
            elif choice == '3' and graph.is_weighted:
                matrix, nodes = matrix_analyzer.get_weight_matrix()
                if matrix:
                    matrix_analyzer.print_weight_matrix()
                    matrix_analyzer.interactive_matrix_operations(matrix, nodes, "Matice vah")
                else:
                    print("Matice vah je prázdná")
        except KeyboardInterrupt:
            print("\nPřerušeno uživatelem")
        return

    if not show_any_specific:
        matrix_analyzer.print_adjacency_matrix()
        matrix_analyzer.print_incidence_matrix()
        if graph.is_weighted:
            matrix_analyzer.print_weight_matrix()
        if export_dir:
            A, nodes = matrix_analyzer.get_adjacency_matrix()
            path = os.path.join(export_dir, 'adjacency.csv')
            matrix_analyzer.save_matrix_csv(A, nodes, col_labels=nodes, path=path)
            I, nodes, edges = matrix_analyzer.get_incidence_matrix()
            path = os.path.join(export_dir, 'incidence.csv')
            matrix_analyzer.save_matrix_csv(I, nodes, col_labels=[f'e{i+1}' for i in range(len(edges))], path=path)
            if graph.is_weighted:
                W, nodes = matrix_analyzer.get_weight_matrix()
                path = os.path.join(export_dir, 'weight.csv')
                matrix_analyzer.save_matrix_csv(W, nodes, col_labels=nodes, path=path)
        return

    if '--adjacency' in sys.argv:
        matrix_analyzer.print_adjacency_matrix()
        if export_dir:
            A, nodes = matrix_analyzer.get_adjacency_matrix()
            matrix_analyzer.save_matrix_csv(A, nodes, col_labels=nodes, path=os.path.join(export_dir, 'adjacency.csv'))
    if '--incidence' in sys.argv:
        matrix_analyzer.print_incidence_matrix()
        if export_dir:
            I, nodes, edges = matrix_analyzer.get_incidence_matrix()
            matrix_analyzer.save_matrix_csv(I, nodes, col_labels=[f'e{i+1}' for i in range(len(edges))], path=os.path.join(export_dir, 'incidence.csv'))
    if '--weight' in sys.argv and graph.is_weighted:
        matrix_analyzer.print_weight_matrix()
        if export_dir:
            W, nodes = matrix_analyzer.get_weight_matrix()
            matrix_analyzer.save_matrix_csv(W, nodes, col_labels=nodes, path=os.path.join(export_dir, 'weight.csv'))
    if '--adj-power' in sys.argv:
        try:
            k_idx = sys.argv.index('--adj-power') + 1
            k = int(sys.argv[k_idx])
            A_k, nodes = matrix_analyzer.get_adjacency_power(k)
            print(f"\nMatice sousednosti ^{k}:")
            matrix_analyzer._print_matrix(A_k, nodes, col_labels=nodes)
            if export_dir:
                matrix_analyzer.save_matrix_csv(A_k, nodes, col_labels=nodes, path=os.path.join(export_dir, f'adjacency_power_{k}.csv'))
        except Exception as e:
            print(f"Chyba při výpočtu A^k: {e}")
