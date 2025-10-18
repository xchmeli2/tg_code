import argparse
import sys
import os

from graph_analyzer import cli

try:
    from graph_analyzer import cli
except ImportError:
    print("Chyba: Balíček 'graph_analyzer' nebyl nalezen.", file=sys.stderr)
    print("Ujistěte se, že spouštíte skript z kořenového adresáře projektu.", file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    cli.run()
