"""
# Python Skript pro Analýzu Grafů

Tento dokument popisuje Python skript pro analýzu grafů, který byl refaktorován do modulární struktury pro lepší organizaci a rozšiřitelnost. Skript je navržen pro parsování grafů z textového souboru a následnou analýzu jejich vlastností a charakteristik, včetně maticových reprezentací a pokročilejších metrik, jak bylo probráno v prvních dvou cvičeních teorie grafů.

## Obsah
1.  [Úvod](#úvod)
2.  [Použití](#použití)
3.  [Formát Vstupního Souboru](#formát-vstupního-souboru)
4.  [Struktura Kódu](#struktura-kódu)
    *   [Balíček `models`](#balíček-models)
    *   [Balíček `utils`](#balíček-utils)
    *   [Balíček `analyzers`](#balíček-analyzers)
    *   [Hlavní skript `main.py`](#hlavní-skript-mainpy)
5.  [Implementované Funkce](#implementované-funkce)
    *   [Základní Vlastnosti Grafu (`GraphPropertiesAnalyzer`)](#základní-vlastnosti-grafu-graphpropertiesanalyzer)
    *   [Charakteristiky Uzlů (přes `Graph` třídu)](#charakteristiky-uzlů-přes-graph-třídu)
    *   [Cesty a Vzdálenosti (`PathAnalyzer`)](#cesty-a-vzdálenosti-pathanalyzer)
    *   [Maticové Reprezentace (`MatrixAnalyzer`)](#maticové-reprezentace-matrixanalyzer)
6.  [Příklady Použití CLI](#příklady-použití-cli)

## Úvod

Cílem tohoto skriptu je poskytnout modulární a rozšiřitelný nástroj pro studenty teorie grafů, který jim umožní snadno analyzovat grafy definované v textovém formátu. Skript automaticky detekuje klíčové vlastnosti grafu a uzlů, což usnadňuje pochopení teoretických konceptů a přípravu na praktické úlohy. Díky modulární struktuře je možné snadno přidávat nové analytické funkce a selektivně spouštět pouze požadované analýzy.

## Použití

Skript se spouští z příkazové řádky pomocí wrapper skriptu `analyze_graph.py` s cestou k vstupnímu textovému souboru obsahujícímu definici grafu a volitelnými argumenty pro specifikaci požadovaných analýz. Při spuštění se v terminálu zobrazí barevný úvodní header.

```bash
./analyze_graph.py <cesta_k_vstupnimu_souboru.txt> [argumenty_analýzy]
```

**Příklad základního použití (kompletní analýza):**

```bash
./analyze_graph.py test_graph.txt --full
```

**Příklad pro zobrazení pouze vlastností grafu:**

```bash
./analyze_graph.py test_graph.txt --properties
```

**Příklad pro nalezení nejkratší cesty:**

```bash
./analyze_graph.py test_graph.txt --path A B
```

# Analyzátor grafů (graph_analyzer)

Jednoduchý nástroj pro analýzu grafů ze zjednodušeného textového formátu. Tento README obsahuje rychlé pokyny a odkazy na podrobnější nápovědu.

Hlavní body
-----------

- Spouštění: `python3 main.py <vstupní_soubor.tg>`
- Pro krátkou referenci příkazů otevřete `HELP.md` v kořenovém adresáři repozitáře.

Rychlé příklady
---------------

Základní analýza (výchozí):

```bash
python3 main.py graphs/example.tg
```

Zobrazit pouze vlastnosti grafu:

```bash
python3 main.py graphs/example.tg --properties
```

Zobrazit informace o uzlu `A`:

```bash
python3 main.py graphs/example.tg --info A
```

Export matic do CSV:

```bash
python3 main.py graphs/example.tg --matrices --export-csv out_csv
```

Formát vstupního souboru (stručně)
---------------------------------

- `u <id> [value];` — definice uzlu
- `h <u> (< | - | >) <v> [weight] [:label];` — definice hrany

Příklad:

```
u A;
u B;
u C;
h A - B;
h B > C [2.5];
```

Struktura projektu
------------------

```
graph_analyzer/
├── cli.py        # parser a run loop
├── commands.py   # orchestrace analýz a tisk výsledků
├── models/       # Node, Edge, Graph
├── utils/        # parser vstupních souborů
└── analyzers/    # vlastnosti, cesty, matice
```

Další nápověda
--------------

Podrobné příklady a stručnou referenční příručku najdete v `HELP.md`.

Chcete-li, mohu také:

- Rozšířit `HELP.md` o další praktické příklady.
- Přidat jednoduché unit testy pro CLI a analyzátory.

Licence: výukové účely — přidejte vhodnou licenci podle potřeby.

*   **`paths.py`**: Definuje třídu `PathAnalyzer` pro analýzu cest a vzdáleností v grafu (např. nejkratší cesta, všechny cesty, excentricita, průměr, poloměr, centrální uzly).
*   **`matrices.py`**: Definuje třídu `MatrixAnalyzer` pro generování a tisk maticových reprezentací grafu (matice sousednosti, matice incidence, matice vah).

### Hlavní skript `main.py`

Slouží jako vstupní bod pro spouštění analýz z příkazové řádky. Používá `argparse` pro zpracování argumentů a koordinuje práci mezi `GraphParser`, `Graph` a jednotlivými analyzátory.

## Implementované Funkce

# Analyzátor grafů (graph_analyzer)

Tento repozitář obsahuje jednoduchý, modulární Python nástroj pro analýzu grafů ze zjednodušeného textového formátu.

Hlavní změny
-------------
- CLI byl zjednodušen a parser byl extrahován do `graph_analyzer.cli.create_parser()`.
- Hlavní vstupní skript pro spouštění je `main.py` (použijte `python3 main.py <soubor>`).
- Doplňková krátká nápověda je v `HELP.md` (stručné příklady a rychlé reference).

Rychlé použití
--------------
Spuštění kompletní analýzy (pokud nejsou zadány konkrétní přepínače):

```bash
python3 main.py graphs/example.tg
```

Zobrazení pouze vlastností grafu:

```bash
python3 main.py graphs/example.tg --properties
```

Zobrazení informací o konkrétním uzlu `A`:

```bash
python3 main.py graphs/example.tg --info A
```

Pro úplnou referenci příkazů otevřete `HELP.md`.

Formát vstupních souborů
-----------------------
Vstupní soubory jsou textové a používají jednoduchý formát se záznamy uzlů (`u`) a hran (`h`). Stručný přehled:

- `u <id> [value];` — definice uzlu
- `h <u> (< | - | >) <v> [weight] [:label];` — definice hrany

Příklad malého grafu:

```
u A;
u B;
u C;
h A - B;
h B > C [2.5];
```

Struktura kódu
--------------
Projekt je rozdělen do modulů:

```
graph_analyzer/
├── cli.py            # parser a run loop
├── commands.py       # orchestrace analýz a tisk výsledků
├── models/           # Node, Edge, Graph
├── utils/            # parser vstupních souborů
└── analyzers/        # vlastnosti, cesty, matice
```

Další kroky
-----------
- Pokud chcete, můžu rozšířit `HELP.md` o další příklady a tipy (provedl jsem základní rozšíření).
- Mohu také vytvořit jednoduché unit testy pro CLI a analyzátory.

Licence
-------
Projekt je pro výukové účely; přidejte vlastní licenci podle potřeby.
