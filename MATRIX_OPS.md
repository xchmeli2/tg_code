# Operace s maticemi

Tento dokument popisuje novou funkcionalitu pro práci s maticemi v Graph Analyzer.

## Interaktivní režim

Pro spuštění interaktivního režimu s maticemi použijte:

```bash
python main.py graphs/01.tg --matrix-ops
```

### Dostupné operace

Po spuštění se zobrazí menu pro výběr matice:
1. **Matice sousednosti** - zobrazuje počet hran mezi uzly
2. **Matice incidence** - vztah mezi uzly a hranami
3. **Matice vah** - vzdálenosti/váhy mezi uzly (pouze pro ohodnocené grafy)

Po výběru matice máte k dispozici následující operace:

#### 1. Součet řádku
Sečte všechny hodnoty v daném řádku matice (odpovídá uzlu).

**Příklad použití:** 
- Pro matici sousednosti: Celkový počet hran vycházejících z uzlu
- Pro matici vah: Součet vah všech přímých spojení z uzlu

#### 2. Součet sloupce
Sečte všechny hodnoty v daném sloupci matice.

**Příklad použití:**
- Pro matici sousednosti: Celkový počet hran vcházejících do uzlu
- Pro matici vah: Součet vah všech přímých spojení do uzlu

#### 3. Součet hlavní diagonály
Sečte prvky na hlavní diagonále (levý horní → pravý dolní).

**Příklad použití:**
- Pro matici sousednosti: Počet smyček v grafu
- Pro matici vah: Stopa matice (vždy 0 pro matici vah)

#### 4. Součet vedlejší diagonály
Sečte prvky na vedlejší diagonále (pravý horní → levý dolní).

#### 5. Celkový součet matice
Sečte všechny hodnoty v celé matici.

**Příklad použití:**
- Pro matici sousednosti: Celkový počet hran v grafu (pokud neorientovaný, pak 2× počet hran)
- Pro matici vah: Součet všech vah

#### 6. Transpozice
Zobrazí transponovanou matici (řádky ↔ sloupce).

**Význam:**
- Pro matici sousednosti: Graf s opačnou orientací hran
- Symetrická matice → graf je neorientovaný

#### 7. Kontrola symetrie
Zkontroluje, zda je matice symetrická.

**Význam:**
- Symetrická matice sousednosti → graf je neorientovaný
- Asymetrická matice → graf je orientovaný nebo obsahuje různé váhy v různých směrech

#### 8. Stopa matice (trace)
Vypočítá stopu matice (součet prvků na hlavní diagonále).

**Význam:**
- Stejné jako součet hlavní diagonály
- Pro matici sousednosti: počet smyček

#### 9. Zobrazit matici znovu
Znovu zobrazí aktuální matici pro referenci.

#### 10. Vyhledat hodnotu
Najde všechny buňky s konkrétní hodnotou.

**Příklad použití:**
- Najít všechny hrany s váhou 5
- Najít všechny smyčky (hodnota na diagonále)
- Najít nedostupné uzly (nekonečno)

#### 11. Vyhledat rozsah hodnot
Najde všechny buňky s hodnotami v daném rozsahu.

**Příklad použití:**
- Najít hrany s váhou mezi 10 a 20
- Najít slabé spojení (malé hodnoty)

#### 12. Najít maximum
Najde maximální hodnotu v matici a všechny pozice, kde se vyskytuje.

**Příklad použití:**
- Nejdelší/nejtěžší hrana v grafu
- Nejvyšší počet paralelních hran mezi dvojicí uzlů

#### 13. Najít minimum
Najde minimální hodnotu v matici a všechny pozice, kde se vyskytuje.

**Příklad použití:**
- Nejkratší/nejlehčí hrana v grafu
- Nejslabší spojení

#### 14. Najít nenulové hodnoty
Zobrazí všechny nenulové buňky (užitečné pro řídké matice).

**Příklad použití:**
- Rychlý přehled všech hran v grafu
- Identifikace existujících spojení

#### 15. Zobrazit hodnotu na pozici [řádek, sloupec]
Přímý přístup k hodnotě na konkrétní pozici v matici.

**Příklad použití:**
- Zjistit počet hran mezi uzly A a B: `[0, 1]`
- Zkontrolovat váhu hrany mezi C a D
- Ověřit existenci smyčky na uzlu E (diagonála)

**Podporované formáty:**
- Index (0-based): `0`, `1`, `2`, ...
- ID uzlu: `A`, `B`, `C`, ...
- Lze kombinovat: řádek=`0`, sloupec=`B`

## Příklady použití

### Příklad 1: Analýza stupňů uzlů
```bash
python main.py graphs/01.tg --matrix-ops
# Vyberte: 1 (Matice sousednosti)
# Operace: 1 (Součet řádku) - pro out-degree
# Operace: 2 (Součet sloupce) - pro in-degree
```

### Příklad 2: Kontrola, zda je graf neorientovaný
```bash
python main.py graphs/01.tg --matrix-ops
# Vyberte: 1 (Matice sousednosti)
# Operace: 7 (Kontrola symetrie)
# Výsledek "Ano" znamená, že graf je neorientovaný
```

### Příklad 3: Počet smyček v grafu
```bash
python main.py graphs/01.tg --matrix-ops
# Vyberte: 1 (Matice sousednosti)
# Operace: 3 (Součet hlavní diagonály)
```

### Příklad 4: Celkový počet hran
```bash
python main.py graphs/01.tg --matrix-ops
# Vyberte: 1 (Matice sousednosti)
# Operace: 5 (Celkový součet matice)
# Pro neorientovaný graf: výsledek / 2 = počet hran
# Pro orientovaný graf: výsledek = počet hran
```

### Příklad 5: Vyhledání konkrétní hodnoty
```bash
python main.py graphs/01.tg --matrix-ops
# Vyberte: 1 (Matice sousednosti)
# Operace: 10 (Vyhledat hodnotu)
# Zadejte: 2
# Výstup: Všechny páry uzlů s 2 hranami mezi nimi
```

### Příklad 6: Nalezení nejdelší/nejtěžší hrany
```bash
python main.py graphs/01.tg --matrix-ops
# Vyberte: 3 (Matice vah)
# Operace: 12 (Najít maximum)
# Výstup: Hrana s nejvyšší váhou
```

### Příklad 7: Přehled všech existujících hran
```bash
python main.py graphs/01.tg --matrix-ops
# Vyberte: 1 (Matice sousednosti)
# Operace: 14 (Najít nenulové hodnoty)
# Výstup: Seznam všech párů uzlů s hranou mezi nimi
```

### Příklad 8: Zjistit spojení mezi dvěma konkrétními uzly
```bash
python main.py graphs/01.tg --matrix-ops
# Vyberte: 1 (Matice sousednosti)
# Operace: 15 (Zobrazit hodnotu na pozici)
# Řádek: A (nebo 0)
# Sloupec: B (nebo 1)
# Výstup: Počet hran z A do B
```

### Příklad 9: Kontrola existence smyčky
```bash
python main.py graphs/01.tg --matrix-ops
# Vyberte: 1 (Matice sousednosti)
# Operace: 15 (Zobrazit hodnotu na pozici)
# Řádek: A
# Sloupec: A
# Výstup: Počet smyček na uzlu A (hodnota na diagonále)
```

## Další možnosti rozšíření

V budoucnu by bylo možné přidat:
- Výpočet determinantu (pro čtvercové matice)
- Výpočet hodnosti matice (rank)
- Inverzní matice
- Vlastní čísla a vlastní vektory
- Násobení matic
- Práce s mocninami matic (A^k) interaktivně
- Export výsledků operací do CSV
- Vizualizace matice jako heatmap

## Technické detaily

### Zpracování nekonečna
Pro matice vah, kde není přímé spojení, používá se hodnota `float('inf')`. Tyto hodnoty jsou při sčítání ignorovány.

### Formátování
- Celá čísla: zobrazena bez desetinných míst
- Desetinná čísla: zobrazena s přesností nastavenou v `MatrixAnalyzer.float_precision`
- Nekonečno: zobrazeno jako symbol `∞` (lze změnit v `MatrixAnalyzer.inf_symbol`)

### API pro programové použití

```python
from graph_analyzer.analyzers import MatrixAnalyzer

# Vytvoření analyzátoru
analyzer = MatrixAnalyzer(graph)

# Získání matice
matrix, nodes = analyzer.get_adjacency_matrix()

# Operace
row_sum = analyzer.sum_row(matrix, 0)
col_sum = analyzer.sum_column(matrix, 1)
diag_sum = analyzer.sum_main_diagonal(matrix)
anti_diag_sum = analyzer.sum_anti_diagonal(matrix)
total = analyzer.sum_all(matrix)

# Transformace
transposed = analyzer.transpose(matrix)
is_sym = analyzer.is_symmetric(matrix)
tr = analyzer.trace(matrix)

# Násobení matic
result = analyzer.matrix_multiply(matrix_a, matrix_b)

# Vyhledávání
# Najít buňky s hodnotou 5
results = analyzer.search_in_matrix(matrix, nodes, value=5)

# Najít buňky v rozsahu 10-20
results = analyzer.search_in_matrix(matrix, nodes, min_val=10, max_val=20)

# Najít buňky splňující podmínku
results = analyzer.search_in_matrix(matrix, nodes, condition=lambda v: v > 0 and v < 10)

# Najít maximum/minimum
max_cells = analyzer.find_max_in_matrix(matrix, nodes)
min_cells = analyzer.find_min_in_matrix(matrix, nodes)

# Najít nenulové hodnoty
nonzero = analyzer.find_nonzero_in_matrix(matrix, nodes)

# Přímý přístup k buňce
# Pomocí indexu
cell = analyzer.get_cell_value(matrix, nodes, row=0, col=1)
# Pomocí ID uzlu
cell = analyzer.get_cell_value(matrix, nodes, row='A', col='B')
# Kombinace
cell = analyzer.get_cell_value(matrix, nodes, row=0, col='B')

# Výsledky vyhledávání jsou ve formátu:
# [{'row': 0, 'col': 1, 'row_node': 'A', 'col_node': 'B', 'value': 5}, ...]
# Nebo pro get_cell_value:
# {'row': 0, 'col': 1, 'row_node': 'A', 'col_node': 'B', 'value': 5}
```
