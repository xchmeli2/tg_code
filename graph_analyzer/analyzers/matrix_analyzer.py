"""
Analyzátor pro maticové reprezentace grafu.
"""

class MatrixAnalyzer:
    """
    Třída pro analýzu maticových reprezentací grafu.
    """
    
    def __init__(self, graph):
        """
        Inicializace analyzátoru.
        
        Args:
            graph (Graph): Graf k analýze
        """
        self.graph = graph
    
    def get_adjacency_matrix(self):
        """
        Vrátí matici sousednosti grafu.
        
        Returns:
            tuple: (matrix, node_list) kde matrix je 2D seznam a node_list je seznam identifikátorů uzlů
        """
        if not self.graph.nodes:
            return [], []
        
        node_list = sorted(self.graph.nodes.keys())
        n = len(node_list)
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        
        for i, u_id in enumerate(node_list):
            for j, v_id in enumerate(node_list):
                # Count edges from u to v
                count = 0
                for edge in self.graph.adj[u_id]:
                    if edge.v.identifier == v_id:
                        if self.graph.is_directed:
                            if edge.direction == '>':
                                count += 1
                        else:
                            count += 1
                matrix[i][j] = count
        
        return matrix, node_list
    
    def get_incidence_matrix(self):
        """
        Vrátí matici incidence grafu.
        
        Returns:
            tuple: (matrix, node_list, edge_list)
        """
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
        
        n_nodes = len(node_list)
        n_edges = len(edge_list)
        matrix = [[0 for _ in range(n_edges)] for _ in range(n_nodes)]
        
        for j, edge in enumerate(edge_list):
            u_idx = node_list.index(edge.u.identifier)
            v_idx = node_list.index(edge.v.identifier)
            
            if edge.direction == '>':
                matrix[u_idx][j] = 1   # Outgoing
                matrix[v_idx][j] = -1  # Incoming
            elif edge.direction == '<':
                matrix[u_idx][j] = -1  # Incoming
                matrix[v_idx][j] = 1   # Outgoing
            else:  # Undirected
                matrix[u_idx][j] = 1
                matrix[v_idx][j] = 1
                
            # Handle self-loops
            if edge.u == edge.v:
                matrix[u_idx][j] = 2
        
        return matrix, node_list, edge_list
    
    def get_weight_matrix(self):
        """
        Vrátí matici vah (vzdáleností) grafu.
        
        Returns:
            tuple: (matrix, node_list)
        """
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
        for i, u_id in enumerate(node_list):
            for edge in self.graph.adj[u_id]:
                j = node_list.index(edge.v.identifier)
                weight = edge.weight if edge.weight is not None else 1
                if isinstance(weight, (int, float)):
                    if self.graph.is_directed:
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
        
        print("\nMatice sousednosti:")
        print("    ", end="")
        for node in nodes:
            print(f"{node:>3}", end="")
        print()
        
        for i, node in enumerate(nodes):
            print(f"{node:>3} ", end="")
            for j in range(len(nodes)):
                print(f"{matrix[i][j]:>3}", end="")
            print()
    
    def print_incidence_matrix(self):
        """Vytiskne matici incidence ve čitelném formátu."""
        matrix, nodes, edges = self.get_incidence_matrix()
        if not matrix:
            print("Prázdný graf - žádná matice incidence")
            return
        
        print("\nMatice incidence:")
        print("    ", end="")
        for i, edge in enumerate(edges):
            print(f"e{i+1:>2}", end="")
        print()
        
        for i, node in enumerate(nodes):
            print(f"{node:>3} ", end="")
            for j in range(len(edges)):
                print(f"{matrix[i][j]:>3}", end="")
            print()
    
    def print_weight_matrix(self):
        """Vytiskne matici vah ve čitelném formátu."""
        matrix, nodes = self.get_weight_matrix()
        if not matrix:
            print("Prázdný graf - žádná matice vah")
            return
        
        print("\nMatice vah:")
        print("      ", end="")
        for node in nodes:
            print(f"{node:>6}", end="")
        print()
        
        for i, node in enumerate(nodes):
            print(f"{node:>3} ", end="")
            for j in range(len(nodes)):
                val = matrix[i][j]
                if val == float('inf'):
                    print(f"{'∞':>6}", end="")
                else:
                    print(f"{val:>6.1f}", end="")
            print()
