Usage
=====

Short reference for the `main.py` CLI (graph_analyzer)

Basic
-----
  ```markdown
  Usage
  =====

  Krátká nápověda pro CLI `main.py` (graph_analyzer)

  Rychlý start
  ------------
  Spusťte kompletní analýzu (výchozí chování, když nejsou zadány specifické přepínače):

    main.py graphs/example.tg

  Zobrazit pouze základní vlastnosti grafu:

    main.py graphs/example.tg --properties

  Zobrazit kompletní analýzu (vlastnosti + matice + základní info):

    main.py graphs/example.tg --full

  Analýzy uzlů
  ------------
  Zobrazit kompletní informace o uzlu `A`:

    main.py graphs/example.tg --info A

  Jiné užitečné příklady:

    main.py graphs/example.tg --neighbors A
    main.py graphs/example.tg --degree B
    main.py graphs/example.tg --successors C
    main.py graphs/example.tg --predecessors D

  Analýzy cest
  ------------
  Krátká cesta mezi `A` a `E`:

    main.py graphs/example.tg --path A E

  Všechny jednoduché cesty mezi `A` a `F` (maximálně N = --max-paths):

    main.py graphs/example.tg --all-paths A F --max-paths 20

  Vzdálenosti od uzlu `A` ke všem ostatním:

    main.py graphs/example.tg --distances A

  Statistiky grafu (průměr, poloměr, centrum):

    main.py graphs/example.tg --diameter
    main.py graphs/example.tg --radius
    main.py graphs/example.tg --center

  Matice a export
  ---------------
  Zobrazit maticové reprezentace (adjacency + incidence [+ weight pokud existují váhy]):

    main.py graphs/example.tg --matrices

  Jen matice sousednosti:

    main.py graphs/example.tg --adjacency

  Interaktivní operace s maticemi (sčítání řádků, sloupců, diagonál, transpozice, ...):

    main.py graphs/example.tg --matrix-ops

  Export do CSV (adresář se vytvoří pokud neexistuje):

    main.py graphs/example.tg --matrices --export-csv out_csv

  Poznámka: CSV soubory se uloží jako `adjacency.csv`, `incidence.csv`, `weight.csv` a případně `adjacency_power_K.csv`.

  python3 main.py graphs/example.tg

  Přepínače a krátká reference
  -----------------------------
    --properties       Zobrazí pouze vlastnosti grafu
    --matrices         Vytiskne maticové reprezentace
    --adjacency        Jen matice sousednosti
    --incidence        Jen matice incidence
    --weight           Jen matice vah
    --adj-power K      Vypočte A^K (počet cest délky K)
    --matrix-ops       Interaktivní operace s maticemi
    --neighbors NODE   Sousedé zadaného uzlu
    --degree NODE      Stupeň zadaného uzlu
    --successors NODE  Následníci (orientované grafy)
    --predecessors NODE Předchůdci (orientované grafy)
    --info NODE        Kompletní informace o uzlu
    --path S E         Nejkratší cesta S -> E
    --all-paths S E    Všechny jednoduché cesty S -> E
    --distances NODE   Vzdálenosti od NODE
    --quiet, -q        Potlačí dekorativní header a oddělovače
    --export-csv out_csv
    --matrix-ops

  Poznámky
  --------
  - Boolean hodnoty se tisknou jako `Ano` / `Ne` a jsou zabarveny pouze pokud je výstup do TTY.
  - `Rovinný (heur.)` je pouze heuristický test (m ≤ 3n−6 pro jednoduché grafy, nebo m ≤ 2n−4 pro bipartitní). Není to plná planarity check.

  Další nápověda
  ---------------
  Plný popis a příklady najdete v `README.md` a v tomto repozitáři v souboru `HELP.md`.

  ```
