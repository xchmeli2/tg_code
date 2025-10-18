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

Další příklady pro maticové reprezentace

```bash
# Vytiskne výchozí sadu matic (sousednost + incidence; přidá se weight pokud graf obsahuje váhy)
./analyze_graph.py test_graph.txt --matrices

# Jen matice sousednosti
./analyze_graph.py test_graph.txt --adjacency

# Matice sousednosti a zároveň A^2 (počet cest délky 2)
./analyze_graph.py test_graph.txt --adjacency --adj-power 2

# Jen matice vah
./analyze_graph.py test_graph.txt --weight

# Export vybraných matic do CSV souborů v adresáři out_dir
./analyze_graph.py test_graph.txt --matrices --export-csv out_dir
```

Poznámky k maticím a CSV exportu

- `MatrixAnalyzer` tiskne matice zarovnané podle šířky sloupců. Plovoucí čísla se formátují s nastavitelnou přesností přes atribut `float_precision` (výchozí 1). Symbol pro reprezentaci "nekonečna" je `∞` (atribut `inf_symbol`). Tyto atributy lze změnit programově před zavoláním tiskových metod.
- CLI přepínače (krátce):
    - `--matrices` — výchozí sada matic (adjacency + incidence; přidá se weight pokud graf obsahuje váhy)
    - `--adjacency` — pouze matice sousednosti
    - `--incidence` — pouze matice incidence
    - `--weight` — pouze matice vah (funguje jen pokud jsou v grafech váhy)
    - `--adj-power K` — spočítá a vytiskne A^K (počet cest délky K)
    - `--export-csv DIR` — uloží vybrané matice do CSV souborů do adresáře `DIR` (vytvoří `adjacency.csv`, `incidence.csv`, `weight.csv` a `adjacency_power_K.csv` pokud je použito `--adj-power`)

CSV formát: první sloupec obsahuje řádkové popisky (identifikátory uzlů), hlavička obsahuje popisky sloupců (uzly nebo `h1,h2,...` pro incidence). Prázdné políčko v CSV znamená žádné přímé spojení (odpovídá `∞` ve výpisu).

## Význam maticových hodnot

Níže krátce popisuji, co jednotlivé hodnoty v jednotlivých maticích znamenají a jak je interpretovat při analýze grafu.

Adjacency (sousednost)

- Tvar: čtvercová matice `n x n`, kde `n` je počet uzlů.
- Hodnoty: nejčastěji `0/1` (0 = žádná bezprostřední hrana, 1 = existuje hrana). V tomto projektu se pro multigrafy používají celá čísla > 0 (počet paralelních hran).
- Diagonála: obvykle `0` (žádná smyčka). Smyčky se mohou projevit jako speciální zápis nebo explicitně v incidence matici.
- Symetrie: pokud je matice symetrická (`A[i][j] == A[j][i]`), graf je neorientovaný. Nesesymetrie indikuje orientované hrany.

Příklad (adjacency):

```
# úplný neorientovaný graf s jednotkovými hranami
[
    [0,1,1],
    [1,0,1],
    [1,1,0]
]
```

Incidence matice

- Tvar: `n_nodes x n_edges` (řádky = uzly, sloupce = hrany).
- Hodnoty v buňkách: `1`, `-1` nebo `2`:
    - `1`  — uzel je zdroj (tail) hrany
    - `-1` — uzel je cíl (head) hrany
    - `2`  — smyčka (hrana spojuje uzel se sebou)

Příklad (incidence pro A->B):

```
# řádky: A, B ; sloupce: e1
[
    [ 1 ],
    [-1 ]
]
```

Matici vah (weight / distance)

- Tvar: čtvercová `n x n` matice.
- Hodnoty: čísla (float nebo int) představují váhy hran. `float('inf')` znamená, že mezi dvěma uzly neexistuje přímá hrana.
- Diagonála je `0`.

Příklad (weight):

```
[
    [0.0,   1.5,    inf],
    [1.5,   0.0,    2.0],
    [inf,   2.0,    0.0]
]
```

CSV mapování a praktické poznámky

- V CSV exportu: prázdné pole = žádné přímé spojení (odpovídá `∞` ve výpisu). Numerická pole obsahují hodnotu přesně tak, jak je v matici.
- U incidence CSV jsou sloupce `h1..hm` a buňky jsou `1/-1/2` podle orientace/smyčky.
- Patterny k rozpoznání:
    - Všechny nediagonální hodnoty `1` v `adjacency` => úplný neorientovaný graf s jednotkovými hranami.
    - Silná asymetrie => orientovaný graf.
    - `get_adjacency_power(k)` s nenulovými hodnotami pro (i,j) znamená existenci cesty délky `k` z i do j.

Krátké doporučení

- Pokud chcete v CSV zapisovat explicitní symbol pro nekonečno (např. `INF`), upravte `save_matrix_csv` tak, aby zapisoval tento řetězec místo prázdného políčka.
- Pro rychlou kontrolu matic otevřete CSV v tabulkovém editoru a hledejte výše popsané patterny (symetrie, prázdné sloupce/řádky, jednotkové matice apod.).
