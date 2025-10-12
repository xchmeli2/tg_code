"""
Analyzátor pro základní vlastnosti grafu.
"""

import collections

class GraphPropertiesAnalyzer:
    """
    Třída pro analýzu základních vlastností grafu.
    """
    
    def __init__(self, graph):
        """
        Inicializace analyzátoru.
        
        Args:
            graph (Graph): Graf k analýze
        """
        self.graph = graph
    
    def is_directed_graph(self):
        """Zjistí, zda je graf orientovaný."""
        return self.graph.is_directed
    
    def is_weighted_graph(self):
        """Zjistí, zda je graf ohodnocený."""
        return self.graph.is_weighted
    
    def is_simple_graph(self):
        """Zjistí, zda je graf prostý (bez smyček a násobných hran)."""
        return not self.graph.has_loops and not self.graph.has_multiple_edges
    
    def is_finite_graph(self):
        """Zjistí, zda je graf konečný (vždy True pro parsované grafy)."""
        return True
    
    def has_loops_graph(self):
        """Zjistí, zda graf obsahuje smyčky."""
        return self.graph.has_loops
    
    def has_multiple_edges_graph(self):
        """Zjistí, zda graf obsahuje násobné hrany."""
        return self.graph.has_multiple_edges
    
    def is_connected_graph(self):
        """Zjistí, zda je graf souvislý (ignoruje placeholder uzly)."""
        # FILTRUJ PLACEHOLDER UZLY
        real_nodes = {node_id for node_id in self.graph.nodes 
                    if not node_id.startswith('*_')}
        
        if not real_nodes:
            return True
        
        # ZAČNI OD PRVNÍHO SKUTEČNÉHO UZLU
        start_node_id = next(iter(real_nodes))
        visited = set()
        queue = collections.deque([start_node_id])
        visited.add(start_node_id)
        
        while queue:
            current_node_id = queue.popleft()
            
            for edge in self.graph.adj[current_node_id]:
                neighbor_id = edge.v.identifier
                # POUZE SKUTEČNÉ UZLY
                if neighbor_id in real_nodes and neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append(neighbor_id)
            
            if self.graph.is_directed:
                for edge in self.graph.rev_adj[current_node_id]:
                    neighbor_id = edge.u.identifier
                    if neighbor_id in real_nodes and neighbor_id not in visited:
                        visited.add(neighbor_id)
                        queue.append(neighbor_id)
        
        # POROVNEJ S POČTEM SKUTEČNÝCH UZLŮ
        return len(visited) == len(real_nodes)

    
    def is_complete_graph(self):
        """Zjistí, zda je graf úplný."""
        num_nodes = len(self.graph.nodes)
        if num_nodes == 0 or num_nodes == 1:
            return True
        
        # A complete graph must be undirected and simple
        if self.graph.is_directed or self.graph.has_loops or self.graph.has_multiple_edges:
            return False
        
        # For each pair of distinct nodes (u, v), there must be exactly one edge
        expected_edges = num_nodes * (num_nodes - 1) // 2
        actual_edges = len(self.graph.edges)
        
        if actual_edges != expected_edges:
            return False
        
        # Verify every pair is connected
        for u_id, u_node in self.graph.nodes.items():
            for v_id, v_node in self.graph.nodes.items():
                if u_id == v_id:
                    continue
                found_edge = False
                for edge in self.graph.adj[u_id]:
                    if edge.v == v_node:
                        found_edge = True
                        break
                if not found_edge:
                    return False
        return True
    
    def is_regular_graph(self):
        """Zjistí, zda je graf regulární (všechny uzly mají stejný stupeň)."""
        if not self.graph.nodes:
            return True
        
        degrees = []
        for node_id in self.graph.nodes:
            if self.graph.is_directed:
                in_degree = len(self.graph.rev_adj[node_id])
                out_degree = len(self.graph.adj[node_id])
                degrees.append(in_degree + out_degree)
            else:
                degrees.append(len(self.graph.adj[node_id]))
        
        if not degrees:
            return True
        
        first_degree = degrees[0]
        return all(d == first_degree for d in degrees)
    
    def is_bipartite_graph(self):
        """Zjistí, zda je graf bipartitní."""
        if not self.graph.nodes:
            return True
        
        # Use BFS to color the graph with two colors
        color = {}
        for node_id in self.graph.nodes:
            if node_id not in color:
                queue = collections.deque([node_id])
                color[node_id] = 0
                
                while queue:
                    u_id = queue.popleft()
                    # Consider all neighbors regardless of edge direction for bipartiteness
                    neighbors = set()
                    for edge in self.graph.adj[u_id]:
                        neighbors.add(edge.v.identifier)
                    if self.graph.is_directed:
                        for edge in self.graph.rev_adj[u_id]:
                            neighbors.add(edge.u.identifier)
                    
                    for v_id in neighbors:
                        if v_id not in color:
                            color[v_id] = 1 - color[u_id]
                            queue.append(v_id)
                        elif color[v_id] == color[u_id]:
                            return False
        return True
    
    def count_components(self):
        """Spočítá počet komponent grafu."""
        if not self.graph.nodes:
            return 0
        
        real_nodes = {node_id for node_id in self.graph.nodes 
            if not node_id.startswith('*_')}
        
        if not real_nodes:
            return 0

        visited = set()
        components = 0
        
        for node_id in real_nodes:
            if node_id not in visited:
                components += 1
                queue = collections.deque([node_id])
                visited.add(node_id)
                
                while queue:
                    current_node_id = queue.popleft()

                    for edge in self.graph.adj[current_node_id]:
                        neighbor_id = edge.v.identifier

                        if neighbor_id in real_nodes and neighbor_id not in visited:
                            visited.add(neighbor_id)
                            queue.append(neighbor_id)

                    if self.graph.is_directed:
                        for edge in self.graph.rev_adj[current_node_id]:
                            neighbor_id = edge.u.identifier
                            if neighbor_id not in visited:
                                visited.add(neighbor_id)
                                queue.append(neighbor_id)
        
        return components
    
    def has_cycles(self):
        """Zjistí, zda graf obsahuje cykly."""
        if not self.graph.nodes:
            return False
        
        if self.graph.is_directed:
            return self._has_cycles_directed()
        else:
            return self._has_cycles_undirected()
    
    def _has_cycles_directed(self):
        """Detekce cyklů v orientovaném grafu pomocí DFS."""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {node_id: WHITE for node_id in self.graph.nodes}
        
        def dfs(node_id):
            if color[node_id] == GRAY:
                return True  # Back edge found, cycle detected
            if color[node_id] == BLACK:
                return False
            
            color[node_id] = GRAY
            for edge in self.graph.adj[node_id]:
                if edge.direction == '>' and dfs(edge.v.identifier):
                    return True
            color[node_id] = BLACK
            return False
        
        for node_id in self.graph.nodes:
            if color[node_id] == WHITE and dfs(node_id):
                return True
        return False
    
    def _has_cycles_undirected(self):
        """Detekce cyklů v neorientovaném grafu pomocí DFS."""
        visited = set()
        
        def dfs(node_id, parent_id):
            visited.add(node_id)
            for edge in self.graph.adj[node_id]:
                neighbor_id = edge.v.identifier
                if neighbor_id not in visited:
                    if dfs(neighbor_id, node_id):
                        return True
                elif neighbor_id != parent_id:
                    return True
            return False
        
        for node_id in self.graph.nodes:
            if node_id not in visited:
                if dfs(node_id, None):
                    return True
        return False
    
    def is_tree(self):
        """Zjistí, zda je graf strom (ignoruje placeholder uzly)."""
        real_nodes = {node_id for node_id in self.graph.nodes 
                    if not node_id.startswith('*_')}
        
        if self.graph.is_directed:
            if self.has_cycles():
                return False
            
            root_candidates = []
            for node_id in real_nodes:  # POUZE SKUTEČNÉ UZLY
                in_degree = len([e for e in self.graph.rev_adj[node_id] 
                            if e.u.identifier in real_nodes])
                if in_degree == 0:
                    root_candidates.append(node_id)
                elif in_degree > 1:
                    return False
            
            if len(root_candidates) != 1:
                return False
            
            return self.is_connected_graph()
        else:
            # Neorientovaný strom
            num_real_nodes = len(real_nodes)
            num_real_edges = len([e for e in self.graph.edges 
                                if (e.u.identifier in real_nodes and 
                                    e.v.identifier in real_nodes)])
            
            if num_real_nodes == 0:
                return True
            if num_real_nodes == 1:
                return num_real_edges == 0
            
            if not self.is_connected_graph():
                return False
            if self.has_cycles():
                return False
            if num_real_edges != num_real_nodes - 1:
                return False
            return True
    
    def is_forest(self):
        """Zjistí, zda je graf les (ignoruje placeholder uzly)."""
        if self.has_cycles():
            return False
        
        real_nodes = {node_id for node_id in self.graph.nodes 
                    if not node_id.startswith('*_')}
        
        num_real_nodes = len(real_nodes)
        num_real_edges = len([e for e in self.graph.edges 
                            if (e.u.identifier in real_nodes and 
                                e.v.identifier in real_nodes)])
        num_components = self.count_components()  # už filtruje placeholder uzly
        
        if num_real_nodes == 0:
            return True
        
        # Pro les: počet_hran = počet_uzlů - počet_komponent
        if num_real_edges != num_real_nodes - num_components:
            return False
        
        return True

    
    def get_basic_properties(self):
        """
        Vrátí slovník se všemi základními vlastnostmi grafu.
        
        Returns:
            dict: Slovník s vlastnostmi grafu
        """
        return {
            'node_count': len(self.graph.nodes),
            'edge_count': len(self.graph.edges),
            'is_directed': self.is_directed_graph(),
            'is_weighted': self.is_weighted_graph(),
            'is_simple': self.is_simple_graph(),
            'is_finite': self.is_finite_graph(),
            'has_loops': self.has_loops_graph(),
            'has_multiple_edges': self.has_multiple_edges_graph(),
            'is_connected': self.is_connected_graph(),
            'is_complete': self.is_complete_graph(),
            'is_regular': self.is_regular_graph(),
            'is_bipartite': self.is_bipartite_graph(),
            'is_tree': self.is_tree(),
            'is_forest': self.is_forest(),
            'has_cycles': self.has_cycles(),
            'component_count': self.count_components()
        }
