import csv
import os

class MatrixAnalyzer:
    """
    - get_adjacency_matrix() -> (matrix, node_list)
        matrix: list[list[int]] velikost n x n, matrix[i][j] = počet hran z i do j
        node_list: seřazené ID uzlů (indexy řádků/sloupců)

    - get_incidence_matrix() -> (matrix, node_list, edge_list)
        matrix: list[list[int]] velikost n_nodes x n_edges, hodnoty 1/-1/2 podle orientace/smyčky
        edge_list: seznam hran odpovídajících sloupcům (unikátní podle (u,v,direction))

    - get_weight_matrix() -> (matrix, node_list)
        matrix: list[list[float]] velikost n x n; neexistující přímé spojení = float('inf'), diagonála = 0

    - get_adjacency_power(k) -> (matrix_k, node_list)
        matrix_k: počet cest délky k mezi dvojicemi uzlů (celá čísla)

    Formátování a export:
    - _print_matrix() zarovnává sloupce podle šířky obsahu
    - _format_cell() používá `self.float_precision` a `self.inf_symbol`
    - save_matrix_csv(...) uloží CSV (prázdná buňka = žádné přímé spojení)

    TODO k rozšíření a výkonu:
    - Pro velké grafy doporučuji vytvořit lokální mapu id->index (dict) a používat ji namísto node_list.index()
    - Pokud chcete dělat numeriku (A^k) pro velké grafy, zvažte numpy arrays pro výkon
    """

    def __init__(self, graph):
        """Inicializace analyzátoru.

        Args:
            graph (Graph): Graf k analýze
        """
        self.graph = graph
        # formatting options
        # float_precision: how many decimal places to show for floating values
        # inf_symbol: symbol used to render 'infinite' / no direct connection
        self.float_precision = 1  # number of decimals to show for floats
        self.inf_symbol = '∞'
    
    """
    Vrátí matici sousednosti grafu.
    
    Returns:
        tuple: (matrix, node_list) kde matrix je 2D seznam a node_list je seznam identifikátorů uzlů
    """
    def get_adjacency_matrix(self):
        # If there are no nodes, return empty structures
        # Returns: (matrix, node_list)
        #  - matrix: n x n list of ints (counts of edges between nodes)
        #  - node_list: sorted list of node identifiers (order of rows/cols)
        if not self.graph.nodes:
            return [], []
        
        node_list = sorted(self.graph.nodes.keys())
        n = len(node_list)
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        
        # Naivní implementace: pro každý pár (u,v) projít sousední hrany u a spočítat
        # počet hran vedoucích do v. To vrací multiplicitu hran mezi dvojicí uzlů.
        # Pozn.: pro velké grafy zvážit vytvoření id->index mapy a iteraci přes adj seznamy (optimalizace).
        for i, u_id in enumerate(node_list):
            for j, v_id in enumerate(node_list):
                # Count edges from u to v
                count = 0
                for edge in self.graph.adj[u_id]:
                    if edge.v.identifier == v_id:
                        if self.graph.is_directed:
                            # pouze explicitně orientované hrany '>' se počítají jako u->v
                            if edge.direction == '>':
                                count += 1
                        else:
                            # v neorientovaném grafu každá hrana mezi uzly zvyšuje hodnotu
                            count += 1
                matrix[i][j] = count
        
        return matrix, node_list
    
    """
    Vrátí matici incidence grafu.
    
    ---

    Returns: tuple: (matrix, node_list, edge_list)
    - matrix: n_nodes x n_edges, hodnoty v buňkách jsou 1 / -1 / 2
    Semantika:
        * 1  — uzel je zvolený "zdroj" hrany (tail)
        * -1 — uzel je zvolený "cíl" hrany (head)
        * 2  — smyčka (edge spojuje uzel se sebou samým; incidenčně se započítává dvakrát)
    Edge cases: prázdný graf nebo bez hran vrátí prázdné struktury
    """
    def get_incidence_matrix(self):
        if not self.graph.nodes or not self.graph.edges:
            return [], [], []

        node_list = sorted(self.graph.nodes.keys())
        edge_list = []

        # Create a list of unique edges (avoid duplicates for undirected)
        seen_edges = set()
        for edge in self.graph.edges:
            edge_key = (edge.u.identifier, edge.v.identifier, edge.direction)
            if edge_key not in seen_edges:
                edge_list.append(edge)
                seen_edges.add(edge_key)

        # Build zero matrix sized by nodes x edges
        n_nodes = len(node_list)
        n_edges = len(edge_list)
        matrix = [[0 for _ in range(n_edges)] for _ in range(n_nodes)]

        # Build a quick lookup map id->index to avoid repeated index() calls
        node_index = {nid: idx for idx, nid in enumerate(node_list)}

        for j, edge in enumerate(edge_list):
            # map node identifiers to row indices
            u_idx = node_index[edge.u.identifier]
            v_idx = node_index[edge.v.identifier]

            # Fill according to orientation
            if edge.direction == '>':
                matrix[u_idx][j] = 1   # Outgoing
                matrix[v_idx][j] = -1  # Incoming
            elif edge.direction == '<':
                matrix[u_idx][j] = -1  # Incoming
                matrix[v_idx][j] = 1   # Outgoing
            else:  # Undirected
                matrix[u_idx][j] = 1
                matrix[v_idx][j] = 1

            # Handle self-loops: represent as 2 in the corresponding column
            if edge.u == edge.v:
                matrix[u_idx][j] = 2

        return matrix, node_list, edge_list
    
    """
    Vrátí matici vah (vzdáleností) grafu.
    
    Returns:
        tuple: (matrix, node_list)
    """
    def get_weight_matrix(self):
        # Returns (matrix, node_list)
        # matrix uses float('inf') for missing direct connection, diagonal 0
        if not self.graph.nodes:
            return [], []
        
        node_list = sorted(self.graph.nodes.keys())
        n = len(node_list)
        # Initialize with infinity for no direct connection
        INF = float('inf')
        matrix = [[INF for _ in range(n)] for _ in range(n)]
        
        # Set diagonal to 0 (distance from node to itself)
        for i in range(n):
            matrix[i][i] = 0
        
        # Fill in direct edge weights
        # Note: if weight is None we use implicit weight = 1
        # If multiple edges exist, we keep the minimum weight between nodes
        for i, u_id in enumerate(node_list):
            for edge in self.graph.adj[u_id]:
                j = node_list.index(edge.v.identifier)
                weight = edge.weight if edge.weight is not None else 1
                if isinstance(weight, (int, float)):
                    if self.graph.is_directed:
                        # only consider directed '>' edges as outgoing
                        if edge.direction == '>':
                            matrix[i][j] = min(matrix[i][j], weight)
                    else:
                        matrix[i][j] = min(matrix[i][j], weight)
                        matrix[j][i] = min(matrix[j][i], weight)
        
        return matrix, node_list
    

    def print_adjacency_matrix(self):
        """Vytiskne matici sousednosti ve čitelném formátu."""
        matrix, nodes = self.get_adjacency_matrix()
        if not matrix:
            print("Prázdný graf - žádná matice sousednosti")
            return
        # Tisk: využíváme univerzální _print_matrix pro hezké zarovnání
        print("\nMatice sousednosti:")
        self._print_matrix(matrix, nodes, col_labels=nodes)
    
    def print_incidence_matrix(self):
        """Vytiskne matici incidence ve čitelném formátu."""
        matrix, nodes, edges = self.get_incidence_matrix()
        if not matrix:
            print("Prázdný graf - žádná matice incidence")
            return
        # Print incidence matrix with generated edge labels e1,e2,...
        print("\nMatice incidence:")
        col_labels = [f"h{idx+1}" for idx in range(len(edges))]
        self._print_matrix(matrix, nodes, col_labels=col_labels)
    
    def print_weight_matrix(self):
        """Vytiskne matici vah ve čitelném formátu."""
        matrix, nodes = self.get_weight_matrix()
        if not matrix:
            print("Prázdný graf - žádná matice vah")
            return
        # Tisk matice vah: _format_cell se postará o vykreslení floatů a symbolu pro inf
        print("\nMatice vah:")
        self._print_matrix(matrix, nodes, col_labels=nodes)

    def get_adjacency_power(self, k):
        """
        Vrátí matici sousednosti umocněnou na k-tou.
        (A^k)[i][j] = počet cest délky k z i do j.
        """
        # Validace vstupu: k musí být >= 1
        if k < 1:
            raise ValueError('k musí být >= 1')

        A, nodes = self.get_adjacency_matrix()
        if not A:
            return [], []

        # Maticové násobení s ignorováním nul pro úsporu operací
        def mat_mult(X, Y):
            n = len(X)
            Z = [[0]*n for _ in range(n)]
            for i in range(n):
                for p in range(n):
                    if X[i][p] == 0:
                        continue
                    xv = X[i][p]
                    for j in range(n):
                        if Y[p][j]:
                            Z[i][j] += xv * Y[p][j]
            return Z

        result = None
        base = A
        exp = k
        while exp > 0:
            if exp & 1:
                result = mat_mult(result, base) if result is not None else [row[:] for row in base]
            base = mat_mult(base, base)
            exp >>= 1

        return result, nodes

    def _format_cell(self, val):
        # Convert numeric / special values to human-readable strings
        # - float('inf') is rendered as configured inf_symbol
        # - ints are rendered without decimal point
        # - floats are rendered with self.float_precision decimal places
        if val == float('inf'):
            return self.inf_symbol
        if isinstance(val, int):
            return str(val)
        try:
            if abs(val - int(val)) < 1e-9:
                # float representing whole number -> render as int
                return str(int(val))
            fmt = f"{{:.{self.float_precision}f}}"
            return fmt.format(val)
        except Exception:
            return str(val)

    def _print_matrix(self, matrix, nodes, col_labels=None):
        # Pretty-print a 2D matrix with column widths computed from content
        if not matrix:
            print('Prázdná matice')
            return
        rows = len(matrix)
        cols = len(matrix[0]) if rows else 0

        # Prepare string table using _format_cell
        table = [[self._format_cell(matrix[i][j]) for j in range(cols)] for i in range(rows)]

        # Compute max width per column (considering content and optional labels)
        col_widths = [max((len(table[i][j]) for i in range(rows)), default=0) for j in range(cols)]
        if col_labels:
            for j, lbl in enumerate(col_labels):
                col_widths[j] = max(col_widths[j], len(str(lbl)))

        # Width for row labels (node ids)
        row_label_width = max((len(str(n)) for n in nodes), default=0)

        # Print header
        print()
        print(' '*(row_label_width+1), end='')
        for j in range(cols):
            lbl = col_labels[j] if col_labels else j+1
            print(f"{str(lbl):>{col_widths[j]+1}}", end='')
        print()

        # Print each row with aligned cells
        for i, node in enumerate(nodes):
            print(f"{str(node):>{row_label_width}} ", end='')
            for j in range(cols):
                print(f"{table[i][j]:>{col_widths[j]+1}}", end='')
            print()

    
    """
    Uloží matici do CSV souboru.

    Args:
        matrix: 2D seznam (rows x cols)
        nodes: seznam identifikátorů uzlů (řádkové popisky)
        col_labels: seznam popisků pro sloupce (volitelné)
        path: cesta k výstupnímu CSV (pokud None vrátí CSV jako string)
    Returns:
        path (str) when written or CSV string when path is None
    """
    def save_matrix_csv(self, matrix, nodes, col_labels=None, path=None):
        rows = len(matrix)
        cols = len(matrix[0]) if rows else 0

        header = [''] + [str(l) for l in (col_labels if col_labels is not None else nodes)]

        table = []
        for i, node in enumerate(nodes):
            row = [str(node)]
            for j in range(cols):
                val = matrix[i][j]
                if val == float('inf'):
                    row.append('')
                else:
                    row.append(str(val))
            table.append(row)

        if path is None:
            from io import StringIO
            sio = StringIO()
            writer = csv.writer(sio)
            writer.writerow(header)
            writer.writerows(table)
            return sio.getvalue()

        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(table)
        return path
