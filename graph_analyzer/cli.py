import argparse
import sys
from . import commands

def print_custom_header():
    header = r"""
╔───────────────────────────────────────────────────────────────╗
│                                                               │
│     ▄████  ██▀███   ▄▄▄       ██▓███   ██░ ██  ██▓ ▒█████     │
│    ██▒ ▀█▒▓██ ▒ ██▒▒████▄    ▓██░  ██▒▓██░ ██▒▓██▒▒██▒  ██▒   │
│   ▒██░▄▄▄░▓██ ░▄█ ▒▒██  ▀█▄  ▓██░ ██▓▒▒██▀▀██░▒██▒▒██░  ██▒   │
│   ░▓█  ██▓▒██▀▀█▄  ░██▄▄▄▄██ ▒██▄█▓▒ ▒░▓█ ░██ ░██░▒██   ██░   │
│   ░▒▓███▀▒░██▓ ▒██▒ ▓█   ▓██▒▒██▒ ░  ░░▓█▒░██▓░██░░ ████▓▒░   │
│    ░▒   ▒ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░▒▓▒░ ░  ░ ▒ ░░▒░▒░▓  ░ ▒░▒░▒░    │
│     ░   ░   ░▒ ░ ▒░  ▒   ▒▒ ░░▒ ░      ▒ ░▒░ ░ ▒ ░  ░ ▒ ▒░    │
│   ░ ░   ░   ░░   ░   ░   ▒   ░░        ░  ░░ ░ ▒ ░░ ░ ░ ▒     │
│         ░    ░           ░  ░          ░  ░  ░ ░      ░ ░     │
│                                                               │
╚───────────────────────────────────────────────────────────────╝
    """
    print(header)

def create_parser():
    """Vytvoří parser pro argumenty příkazové řádky."""
    parser = argparse.ArgumentParser(
                description='Analyzátor grafů - nástroj pro analýzu vlastností a charakteristik grafů',
                formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog="""
Stručný přehled všech funkcí):

=====================================
            Základní:
=====================================


    %(prog)s graf.txt
    -------------------------------------------------------------------------------------------------------------------------------
        Vytiskne základní informace (počet uzlů/hran) a vlastnosti grafu.


=====================================
        Vlastnosti grafu:
=====================================


    %(prog)s graf.txt --properties
    -------------------------------------------------------------------------------------------------------------------------------
        Jen základní vlastnosti (directed/weighted/simple/connected/complete/regular/bipartite/tree/forest/cycles/components)

        
=====================================
           Analýza uzlů:
=====================================


    %(prog)s graf.txt --neighbors A
    -------------------------------------------------------------------------------------------------------------------------------
        Zobrazí všechny sousedy uzlu A (ignoruje směr hran).

    %(prog)s graf.txt --degree A
    -------------------------------------------------------------------------------------------------------------------------------
        Zobrazí stupeň uzlu A (in/out/total pro orientované grafy).

    %(prog)s graf.txt --successors A
    -------------------------------------------------------------------------------------------------------------------------------
        Následníci uzlu A (u->v, orientované hrany).

    %(prog)s graf.txt --predecessors A
    -------------------------------------------------------------------------------------------------------------------------------
        Předchůdci uzlu A (v->u, orientované hrany).

        
=====================================
           Analýzy cest:
=====================================


    %(prog)s graf.txt --path A B
    -------------------------------------------------------------------------------------------------------------------------------
        Najde nejkratší cestu z A do B (BFS pro neohodnocené, Dijkstra pro ohodnocené grafy).

    %(prog)s graf.txt --all-paths A B
    -------------------------------------------------------------------------------------------------------------------------------
        Najde všechny jednoduché cesty mezi A a B (omezeno parametrem --max-paths).

    %(prog)s graf.txt --distances A
    -------------------------------------------------------------------------------------------------------------------------------
        Vzdálenosti od uzlu A ke všem ostatním.

    %(prog)s graf.txt --diameter
    -------------------------------------------------------------------------------------------------------------------------------
        Průměr grafu (max z excentricit). Pokud graf není souvislý, vrací nekonečno.

    %(prog)s graf.txt --radius
    -------------------------------------------------------------------------------------------------------------------------------
        Poloměr grafu.

    %(prog)s graf.txt --center
    -------------------------------------------------------------------------------------------------------------------------------
        Centrální uzly grafu.

        
=====================================
        Maticové reprezentace:
=====================================


    %(prog)s graf.txt --matrices
    -------------------------------------------------------------------------------------------------------------------------------
        Vytiskne adjacency + incidence (a weight pokud graf má váhy).
    %(prog)s graf.txt --adjacency
    -------------------------------------------------------------------------------------------------------------------------------
        Jen matice sousednosti.

    %(prog)s graf.txt --incidence
    -------------------------------------------------------------------------------------------------------------------------------
        Jen incidence matice.

    %(prog)s graf.txt --weight
    -------------------------------------------------------------------------------------------------------------------------------
        Jen matice vah (pouze pokud jsou váhy přítomné).

    %(prog)s graf.txt --adj-power 2
    -------------------------------------------------------------------------------------------------------------------------------
        Vypočte A^2 (počet cest délky 2).

    %(prog)s graf.txt --matrices --export-csv out_dir
    -------------------------------------------------------------------------------------------------------------------------------
        Exportuje matice do CSV souborů v adresáři out_dir.

        
=====================================
     Další užitečné přepínače:
=====================================


    %(prog)s graf.txt --quiet
    -------------------------------------------------------------------------------------------------------------------------------
        Potlačí dekorativní výstup (jen výsledky).

    %(prog)s graf.txt --max-paths 50
    -------------------------------------------------------------------------------------------------------------------------------
        Zvětší limit počtu zobrazených cest při --all-paths.


    """
    )

    parser.add_argument('input_file', help='Cesta k vstupnímu souboru s definicí grafu')
    analysis_group = parser.add_argument_group('Typy analýz')
    analysis_group.add_argument('--properties', action='store_true', help='Zobrazí základní vlastnosti grafu')
    analysis_group.add_argument('--matrices', action='store_true', help='Zobrazí maticové reprezentace grafu')
    analysis_group.add_argument('--adjacency', action='store_true', help='Zobrazí matici sousednosti (pouze)')
    analysis_group.add_argument('--incidence', action='store_true', help='Zobrazí matici incidence (pouze)')
    analysis_group.add_argument('--weight', action='store_true', help='Zobrazí matici vah (pouze)')
    analysis_group.add_argument('--adj-power', type=int, metavar='K', help='Vypočte matici sousednosti na K-tou (A^K)')
    analysis_group.add_argument('--full', action='store_true', help='Zobrazí kompletní analýzu grafu')

    node_group = parser.add_argument_group('Analýzy uzlů')
    node_group.add_argument('--neighbors', metavar='NODE', help='Zobrazí sousedy zadaného uzlu')
    node_group.add_argument('--degree', metavar='NODE', help='Zobrazí stupeň zadaného uzlu')
    node_group.add_argument('--successors', metavar='NODE', help='Zobrazí následníky zadaného uzlu (orientované grafy)')
    node_group.add_argument('--predecessors', metavar='NODE', help='Zobrazí předchůdce zadaného uzlu (orientované grafy)')

    path_group = parser.add_argument_group('Analýzy cest')
    path_group.add_argument('--path', nargs=2, metavar=('START', 'END'), help='Najde nejkratší cestu mezi dvěma uzly')
    path_group.add_argument('--all-paths', nargs=2, metavar=('START', 'END'), help='Najde všechny jednoduché cesty mezi dvěma uzly')
    path_group.add_argument('--distances', metavar='NODE', help='Zobrazí vzdálenosti od zadaného uzlu ke všem ostatním')
    path_group.add_argument('--diameter', action='store_true', help='Vypočítá průměr grafu')
    path_group.add_argument('--radius', action='store_true', help='Vypočítá poloměr grafu')
    path_group.add_argument('--center', action='store_true', help='Najde centrální uzly grafu')

    parser.add_argument('--quiet', '-q', action='store_true', help='Potlačí výstupní zprávy (pouze výsledky)')
    parser.add_argument('--export-csv', metavar='DIR', help='Exportovat vybrané matice jako CSV do adresáře DIR')
    parser.add_argument('--max-paths', type=int, default=10, metavar='N', help='Maximální počet zobrazených cest (výchozí: 10)')

    return parser


def run(argv=None):
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.quiet:
        print_custom_header()

    graph = commands.load_graph(args.input_file)

    has_specific_args = any([
        args.properties, args.matrices, args.full,
        args.neighbors, args.degree, args.successors, args.predecessors,
        args.path, args.all_paths, args.distances, args.diameter, args.radius, args.center,
        args.adjacency, args.incidence, args.weight, args.adj_power is not None
    ])

    if not has_specific_args:
        commands.print_basic_info(graph, args.quiet)
        commands.analyze_properties(graph, args.quiet)
        return

    if not args.quiet:
        commands.print_basic_info(graph, args.quiet)

    if args.properties or args.full:
        commands.analyze_properties(graph, args.quiet)

    if args.neighbors:
        commands.analyze_node(graph, args.neighbors, 'neighbors', args.quiet)

    if args.degree:
        commands.analyze_node(graph, args.degree, 'degree', args.quiet)

    if args.successors:
        commands.analyze_node(graph, args.successors, 'successors', args.quiet)

    if args.predecessors:
        commands.analyze_node(graph, args.predecessors, 'predecessors', args.quiet)

    if any([args.path, args.all_paths, args.distances, args.diameter, args.radius, args.center]):
        commands.analyze_paths(graph, args, args.quiet)

    specific_matrix_flags = any([args.adjacency, args.incidence, args.weight, args.adj_power is not None])
    if args.matrices or args.full or specific_matrix_flags:
        commands.analyze_matrices(graph, args, args.quiet)
