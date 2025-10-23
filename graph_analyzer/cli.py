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
    lines = header.splitlines()
    # If not a TTY, print without colors
    if not sys.stdout.isatty():
        print(header)
        return

    n = len(lines)
    if n <= 1:
        print(header)
        return

    for i, line in enumerate(lines):
        # compute a red gradient from bright (255) to darker (120)
        t = i / (n - 1)
        r = int(255 - t * 135)           # 255 -> 120
        g = int(r * 0.12)                # keep slight warmth
        b = int(r * 0.06)
        # clamp
        r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
        sys.stdout.write(f"\x1b[38;2;{r};{g};{b}m{line}\x1b[0m\n")


def create_parser():
    """Create argparse.ArgumentParser with CLI options."""
    parser = argparse.ArgumentParser(
        description='Analyzátor grafů - nástroj pro analýzu vlastností a charakteristik grafů',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "See HELP.md in the repository for a concise command reference.\n"
            "Examples:\n"
            "  main.py graph.txt --properties\n"
            "  main.py graph.txt --info A\n"
            "  main.py graph.txt --matrices --export-csv out_dir\n"
        ),
    )

    parser.add_argument('input_file', help='Cesta k vstupnímu souboru s definicí grafu')
    analysis_group = parser.add_argument_group('Typy analýz')
    analysis_group.add_argument('--properties', action='store_true', help='Zobrazí základní vlastnosti grafu')
    analysis_group.add_argument('--matrices', action='store_true', help='Zobrazí maticové reprezentace grafu')
    analysis_group.add_argument('--adjacency', action='store_true', help='Zobrazí matici sousednosti (pouze)')
    analysis_group.add_argument('--incidence', action='store_true', help='Zobrazí matici incidence (pouze)')
    analysis_group.add_argument('--weight', action='store_true', help='Zobrazí matici vah (pouze)')
    analysis_group.add_argument('--adj-power', type=int, metavar='K', help='Vypočte matici sousednosti na K-tou (A^K)')
    analysis_group.add_argument('--matrix-ops', action='store_true', help='Interaktivní operace s maticemi (sčítání řádků, sloupců, diagonál, atd.)')
    analysis_group.add_argument('--full', action='store_true', help='Zobrazí kompletní analýzu grafu')

    node_group = parser.add_argument_group('Analýzy uzlů')
    node_group.add_argument('--neighbors', metavar='NODE', help='Zobrazí sousedy zadaného uzlu')
    node_group.add_argument('--degree', metavar='NODE', help='Zobrazí stupeň zadaného uzlu')
    node_group.add_argument('--successors', metavar='NODE', help='Zobrazí následníky zadaného uzlu (orientované grafy)')
    node_group.add_argument('--predecessors', metavar='NODE', help='Zobrazí předchůdce zadaného uzlu (orientované grafy)')
    node_group.add_argument('--info', metavar='NODE', help='Zobrazí všechny vlastnosti zadaného uzlu')

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

    # if not args.quiet:
    #     print_custom_header()

    graph = commands.load_graph(args.input_file)

    has_specific_args = any([
        args.properties, args.matrices, args.full,
        args.neighbors, args.degree, args.successors, args.predecessors, args.info,
        args.path, args.all_paths, args.distances, args.diameter, args.radius, args.center,
        args.adjacency, args.incidence, args.weight, args.adj_power is not None, args.matrix_ops
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

    if args.info:
        commands.analyze_node(graph, args.info, 'all', args.quiet)

    if any([args.path, args.all_paths, args.distances, args.diameter, args.radius, args.center]):
        commands.analyze_paths(graph, args, args.quiet)

    specific_matrix_flags = any([args.adjacency, args.incidence, args.weight, args.adj_power is not None])
    if args.matrices or args.full or specific_matrix_flags or args.matrix_ops:
        commands.analyze_matrices(graph, args, args.quiet)
