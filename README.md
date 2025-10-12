"""
# Dokumentace Python Skriptu pro Analýzu Grafů

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

## Formát Vstupního Souboru

Vstupní soubor je textový soubor, kde každý řádek definuje uzel nebo hranu. Formát je následující:

*   **Uzel:** `u <identifikátor> [ohodnocení];` nebo `u <identifikátor> <ohodnocení>;` nebo `u <identifikátor>;`
    *   `<identifikátor>`: Libovolný řetězec (např. `A`, `node1`, `start`).
    *   `[ohodnocení]` nebo `<ohodnocení>`: Volitelné číselné (celé nebo desetinné, kladné/záporné) nebo řetězcové ohodnocení uzlu. Může být v hranatých závorkách nebo odděleno mezerou.

*   **Hrana:** `h <uzel1> (< | - | >) <uzel2> [ohodnocení] [:označení];`
    *   `<uzel1>`, `<uzel2>`: Identifikátory uzlů, které hrana spojuje.
    *   `(< | - | >)`: Symbol určující směr hrany:
        *   `>`: Orientovaná hrana z `uzel1` do `uzel2`.
        *   `<`: Orientovaná hrana z `uzel2` do `uzel1`.
        *   `-`: Neorientovaná hrana mezi `uzel1` a `uzel2`.
    *   `[ohodnocení]`: Volitelné číselné (celé nebo desetinné, kladné/záporné) ohodnocení hrany v hranatých závorkách.
    *   `[:označení]`: Volitelné řetězcové označení hrany, začínající dvojtečkou.

**Příklady řádků:**

```
u A;
u B 5;
u C [10.5];
h A > B [2.5] :hrana1;
h B - C;
h C < A 3;
```

**Důležité poznámky k formátu:**
*   Pořadí řádků ve vstupním souboru může být libovolné, s výjimkou, že hrana může být použita až v okamžiku, kdy existují potřebné uzly.
*   Uzly binárního stromu jsou zadávány chronologicky po jednotlivých patrech. Hvězdička (`*`) značí „vynechaný“ uzel (tato funkcionalita není v aktuální verzi skriptu plně implementována pro parsování, ale je zmíněna v materiálech).

## Struktura Kódu

Skript je nyní organizován do modulární struktury s následujícími balíčky a soubory:

```
graph_analyzer/
├── __init__.py
├── main.py
├── models/
│   ├── __init__.py
│   ├── node.py
│   ├── edge.py
│   └── graph.py
├── utils/
│   ├── __init__.py
│   └── parser.py
└── analyzers/
    ├── __init__.py
    ├── properties.py
    ├── paths.py
    └── matrices.py
```

### Balíček `models`

Obsahuje základní datové struktury pro reprezentaci grafů.

*   **`node.py`**: Definuje třídu `Node` pro reprezentaci uzlů grafu.
    *   `identifier`: Unikátní identifikátor uzlu (řetězec).
    *   `value`: Volitelné ohodnocení uzlu.
*   **`edge.py`**: Definuje třídu `Edge` pro reprezentaci hran grafu.
    *   `u`, `v`: Objekty `Node` představující počáteční a koncový uzel hrany.
    *   `direction`: Směr hrany (`>`, `<`, `-`).
    *   `weight`: Volitelné číselné ohodnocení hrany.
    *   `label`: Volitelné řetězcové označení hrany.
*   **`graph.py`**: Definuje třídu `Graph`, která agreguje uzly a hrany a udržuje základní vlastnosti grafu (např. zda je orientovaný, ohodnocený, má smyčky atd.). Obsahuje také metody pro přidávání uzlů a hran a načítání dat.

### Balíček `utils`

Obsahuje pomocné nástroje, zejména pro parsování vstupních dat.

*   **`parser.py`**: Definuje třídu `GraphParser` s metodami pro parsování textového souboru a extrakci uzlů a hran do objektů `Node` a `Edge`.

### Balíček `analyzers`

Obsahuje různé analytické moduly, které pracují s objektem `Graph` a počítají specifické vlastnosti nebo charakteristiky.

*   **`properties.py`**: Definuje třídu `GraphPropertiesAnalyzer` pro analýzu základních vlastností grafu (např. souvislost, úplnost, bipartitnost, cykly, stromy, lesy).
*   **`paths.py`**: Definuje třídu `PathAnalyzer` pro analýzu cest a vzdáleností v grafu (např. nejkratší cesta, všechny cesty, excentricita, průměr, poloměr, centrální uzly).
*   **`matrices.py`**: Definuje třídu `MatrixAnalyzer` pro generování a tisk maticových reprezentací grafu (matice sousednosti, matice incidence, matice vah).

### Hlavní skript `main.py`

Slouží jako vstupní bod pro spouštění analýz z příkazové řádky. Používá `argparse` pro zpracování argumentů a koordinuje práci mezi `GraphParser`, `Graph` a jednotlivými analyzátory.

## Implementované Funkce

Funkce jsou nyní rozděleny do příslušných tříd analyzátorů nebo jsou součástí třídy `Graph`.

### Základní Vlastnosti Grafu (`GraphPropertiesAnalyzer`)

*   `is_directed_graph()`: Zda je graf orientovaný.
*   `is_weighted_graph()`: Zda má graf ohodnocené hrany.
*   `is_simple_graph()`: Zda je graf prostý (bez smyček a násobných hran).
*   `is_finite_graph()`: Vždy `True` pro parsované grafy.
*   `has_loops_graph()`: Zda graf obsahuje smyčky.
*   `has_multiple_edges_graph()`: Zda graf obsahuje násobné hrany.
*   `is_connected_graph()`: Zda je graf souvislý (slabě souvislý pro orientované grafy).
*   `is_complete_graph()`: Zda je graf úplný.
*   `is_regular_graph()`: Zda je graf regulární (všechny uzly mají stejný stupeň).
*   `is_bipartite_graph()`: Zda je graf bipartitní.
*   `is_tree()`: Zda je graf strom (neorientovaný nebo kořenový orientovaný).
*   `is_forest()`: Zda je graf les.
*   `has_cycles()`: Zda graf obsahuje cykly.
*   `count_components()`: Spočítá počet komponent grafu.

### Charakteristiky Uzlů (přes `Graph` třídu)

*   `get_successors(node_id)`: Vrací seznam identifikátorů následníků uzlu.
*   `get_predecessors(node_id)`: Vrací seznam identifikátorů předchůdců uzlu.
*   `get_neighbors(node_id)`: Vrací seznam identifikátorů sousedů uzlu.
*   `get_node_degree(node_id)`: Vrací slovník se vstupním, výstupním a celkovým stupněm uzlu.
*   `is_isolated_node(node_id)`: Zda je uzel izolovaný.

### Cesty a Vzdálenosti (`PathAnalyzer`)

*   `find_shortest_path(start_id, end_id)`: Najde nejkratší cestu (BFS pro neohodnocené, Dijkstra pro ohodnocené).
*   `find_all_paths(start_id, end_id, max_length=None)`: Najde všechny jednoduché cesty mezi dvěma uzly.
*   `get_shortest_distances(start_id)`: Najde nejkratší vzdálenosti od daného uzlu ke všem ostatním uzlům.
*   `get_node_eccentricity(node_id)`: Vrací excentricitu uzlu.
*   `get_graph_diameter()`: Vrací průměr grafu.
*   `get_graph_radius()`: Vrací poloměr grafu.
*   `find_center_nodes()`: Najde centrální uzly grafu.

### Maticové Reprezentace (`MatrixAnalyzer`)

*   `get_adjacency_matrix()`: Vrací matici sousednosti a seznam uzlů.
*   `get_incidence_matrix()`: Vrací matici incidence, seznam uzlů a seznam hran.
*   `get_weight_matrix()`: Vrací matici vah (vzdáleností) a seznam uzlů.
*   `print_adjacency_matrix()`: Vytiskne matici sousednosti ve čitelném formátu.
*   `print_incidence_matrix()`: Vytiskne matici incidence ve čitelném formátu.
*   `print_weight_matrix()`: Vytiskne matici vah ve čitelném formátu.

## Příklady Použití CLI

Níže jsou uvedeny příklady použití nového CLI rozhraní:

```bash
# Základní vlastnosti grafu (výchozí, pokud nejsou zadány jiné argumenty)
./analyze_graph.py test_graph.txt

# Pouze základní vlastnosti grafu
./analyze_graph.py test_graph.txt --properties

# Zobrazení sousedů uzlu 'A'
./analyze_graph.py test_graph.txt --neighbors A

# Zobrazení stupně uzlu 'B'
./analyze_graph.py test_graph.txt --degree B

# Zobrazení následníků uzlu 'C' (pro orientované grafy)
./analyze_graph.py test_graph.txt --successors C

# Zobrazení předchůdců uzlu 'D' (pro orientované grafy)
./analyze_graph.py test_graph.txt --predecessors D

# Nalezení nejkratší cesty z 'A' do 'E'
./analyze_graph.py test_graph.txt --path A E

# Nalezení všech cest z 'A' do 'F' (s omezením na prvních 10)
./analyze_graph.py test_graph.txt --all-paths A F

# Zobrazení vzdáleností od uzlu 'A' ke všem ostatním
./analyze_graph.py test_graph.txt --distances A

# Výpočet průměru grafu
./analyze_graph.py test_graph.txt --diameter

# Výpočet poloměru grafu
./analyze_graph.py test_graph.txt --radius

# Nalezení centrálních uzlů grafu
./analyze_graph.py test_graph.txt --center

# Zobrazení maticových reprezentací
./analyze_graph.py test_graph.txt --matrices

# Kompletní analýza (zahrnuje vlastnosti, matice a základní info)
./analyze_graph.py test_graph.txt --full

# Tichý režim (potlačí úvodní a nadpisové zprávy)
./analyze_graph.py test_graph.txt --properties --quiet
```

---
