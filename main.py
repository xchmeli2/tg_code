import argparse
import sys
import os

from graph_analyzer.models import Graph
from graph_analyzer.utils import GraphParser
from graph_analyzer.analyzers import GraphPropertiesAnalyzer, PathAnalyzer, MatrixAnalyzer

def create_parser():
    """Vytvoří parser pro argumenty příkazové řádky."""
    parser = argparse.ArgumentParser(
        description='Analyzátor grafů - nástroj pro analýzu vlastností a charakteristik grafů',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Příklady použití:
  %(prog)s graf.txt                           # Základní vlastnosti grafu
  %(prog)s graf.txt --properties              # Pouze vlastnosti grafu
  %(prog)s graf.txt --neighbors A             # Sousedé uzlu A
  %(prog)s graf.txt --path A B                # Nejkratší cesta z A do B
  %(prog)s graf.txt --all-paths A B           # Všechny cesty z A do B
  %(prog)s graf.txt --degree A                # Stupeň uzlu A
  %(prog)s graf.txt --matrices                # Maticové reprezentace
  %(prog)s graf.txt --full                    # Kompletní analýza
        """
    )
    
    parser.add_argument('input_file', help='Cesta k vstupnímu souboru s definicí grafu')
    
    # Skupiny argumentů pro různé typy analýz
    analysis_group = parser.add_argument_group('Typy analýz')
    analysis_group.add_argument('--properties', action='store_true',
                               help='Zobrazí základní vlastnosti grafu')
    analysis_group.add_argument('--matrices', action='store_true',
                               help='Zobrazí maticové reprezentace grafu')
    analysis_group.add_argument('--full', action='store_true',
                               help='Zobrazí kompletní analýzu grafu')
    
    # Analýzy uzlů
    node_group = parser.add_argument_group('Analýzy uzlů')
    node_group.add_argument('--neighbors', metavar='NODE',
                           help='Zobrazí sousedy zadaného uzlu')
    node_group.add_argument('--degree', metavar='NODE',
                           help='Zobrazí stupeň zadaného uzlu')
    node_group.add_argument('--successors', metavar='NODE',
                           help='Zobrazí následníky zadaného uzlu (orientované grafy)')
    node_group.add_argument('--predecessors', metavar='NODE',
                           help='Zobrazí předchůdce zadaného uzlu (orientované grafy)')
    
    # Analýzy cest
    path_group = parser.add_argument_group('Analýzy cest')
    path_group.add_argument('--path', nargs=2, metavar=('START', 'END'),
                           help='Najde nejkratší cestu mezi dvěma uzly')
    path_group.add_argument('--all-paths', nargs=2, metavar=('START', 'END'),
                           help='Najde všechny jednoduché cesty mezi dvěma uzly')
    path_group.add_argument('--distances', metavar='NODE',
                           help='Zobrazí vzdálenosti od zadaného uzlu ke všem ostatním')
    path_group.add_argument('--diameter', action='store_true',
                           help='Vypočítá průměr grafu')
    path_group.add_argument('--radius', action='store_true',
                           help='Vypočítá poloměr grafu')
    path_group.add_argument('--center', action='store_true',
                           help='Najde centrální uzly grafu')
    
    # Další možnosti
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Potlačí výstupní zprávy (pouze výsledky)')
    parser.add_argument('--max-paths', type=int, default=10, metavar='N',
                       help='Maximální počet zobrazených cest (výchozí: 10)')
    
    return parser

def load_graph(input_file):
    """
    Načte graf ze souboru.
    
    Args:
        input_file (str): Cesta k vstupnímu souboru
        
    Returns:
        Graph: Načtený graf
    """
    try:
        nodes_dict, edges_list = GraphParser.parse_file(input_file)
        graph = Graph()
        graph.load_from_data(nodes_dict, edges_list)
        return graph
    except FileNotFoundError as e:
        print(f"Chyba: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Chyba při načítání grafu: {e}", file=sys.stderr)
        sys.exit(1)

def print_basic_info(graph, quiet=False):
    """Vytiskne základní informace o grafu."""
    if not quiet:
        print("="*60)
        print("ZÁKLADNÍ INFORMACE O GRAFU")
        print("="*60)
    
    print(f"Počet uzlů: {graph.get_node_count()}")
    print(f"Počet hran: {graph.get_edge_count()}")

def analyze_properties(graph, quiet=False):
    """Analyzuje vlastnosti grafu."""
    analyzer = GraphPropertiesAnalyzer(graph)
    properties = analyzer.get_basic_properties()
    
    if not quiet:
        print("\n" + "="*60)
        print("VLASTNOSTI GRAFU")
        print("="*60)
    
    print(f"Orientovaný: {properties['is_directed']}")
    print(f"Ohodnocený: {properties['is_weighted']}")
    print(f"Prostý: {properties['is_simple']}")
    print(f"Souvislý: {properties['is_connected']}")
    print(f"Úplný: {properties['is_complete']}")
    print(f"Regulární: {properties['is_regular']}")
    print(f"Bipartitní: {properties['is_bipartite']}")
    print(f"Strom: {properties['is_tree']}")
    print(f"Les: {properties['is_forest']}")
    print(f"Obsahuje cykly: {properties['has_cycles']}")
    print(f"Počet komponent: {properties['component_count']}")

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
            print(f"Vstupní stupeň: {degree_info['in_degree']}")
            print(f"Výstupní stupeň: {degree_info['out_degree']}")
            print(f"Celkový stupeň: {degree_info['total_degree']}")
        else:
            print(f"Stupeň uzlu: {degree_info['total_degree']}")
        print(f"Izolovaný uzel: {graph.is_isolated_node(node_id)}")
    
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
                # Sečti váhy hran na nejkratší cestě
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

def analyze_matrices(graph, quiet=False):
    """Analyzuje maticové reprezentace grafu."""
    matrix_analyzer = MatrixAnalyzer(graph)
    
    if not quiet:
        print(f"\n{'='*60}")
        print("MATICOVÉ REPREZENTACE")
        print("="*60)
    
    matrix_analyzer.print_adjacency_matrix()
    matrix_analyzer.print_incidence_matrix()
    
    if graph.is_weighted:
        matrix_analyzer.print_weight_matrix()

def main():
    """Hlavní funkce."""
    parser = create_parser()
    args = parser.parse_args()

    # Cool header
    if not args.quiet:
        # ANSI escape codes for colors
        RED = "\033[91m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        MAGENTA = "\033[95m"
        CYAN = "\033[96m"
        WHITE = "\033[97m"
        RESET = "\033[0m"
        BOLD = "\033[1m"

        header = f"""
{BOLD}{CYAN}========================================{RESET}
{BOLD}{GREEN}  G R A P H   A N A L Y Z
{RESET}{BOLD}{CYAN}========================================{RESET}
{BOLD}{YELLOW}Nástroj pro analýzu vlastností a charakteristik grafů{RESET}
{BOLD}{CYAN}========================================{RESET}
"""
        print(header)

    # Načtení grafu
    graph = load_graph(args.input_file)

    
    # Pokud nejsou zadány žádné specifické argumenty, zobraz základní informace
    has_specific_args = any([
        args.properties, args.matrices, args.full,
        args.neighbors, args.degree, args.successors, args.predecessors,
        args.path, args.all_paths, args.distances, args.diameter, args.radius, args.center
    ])
    
    if not has_specific_args:
        print_basic_info(graph, args.quiet)
        analyze_properties(graph, args.quiet)
        return
    
    # Základní informace (vždy zobrazit pokud není --quiet)
    if not args.quiet:
        print_basic_info(graph, args.quiet)
    
    # Analýzy podle argumentů
    if args.properties or args.full:
        analyze_properties(graph, args.quiet)
    
    if args.neighbors:
        analyze_node(graph, args.neighbors, 'neighbors', args.quiet)
    
    if args.degree:
        analyze_node(graph, args.degree, 'degree', args.quiet)
    
    if args.successors:
        analyze_node(graph, args.successors, 'successors', args.quiet)
    
    if args.predecessors:
        analyze_node(graph, args.predecessors, 'predecessors', args.quiet)
    
    # Analýzy cest
    if any([args.path, args.all_paths, args.distances, args.diameter, args.radius, args.center]):
        analyze_paths(graph, args, args.quiet)
    
    if args.matrices or args.full:
        analyze_matrices(graph, args.quiet)

if __name__ == '__main__':
    main()
