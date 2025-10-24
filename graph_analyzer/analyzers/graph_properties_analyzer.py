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

    def _is_placeholder(self, node_id):
        """Return True if node_id represents a placeholder node (binary-tree skip markers)."""
        return isinstance(node_id, str) and node_id.startswith('*')

    def _real_node_ids(self):
        """Return set of node ids that are real (not placeholders)."""
        return {nid for nid in self.graph.nodes if not self._is_placeholder(nid)}

    # Node-level helper methods (convenience API)
    def get_successors(self, node_id):
        """Return list of successor node ids (edges u->v)."""
        return [edge.v.identifier for edge in self.graph.adj.get(node_id, [])]

    def get_predecessors(self, node_id):
        """Return list of predecessor node ids (edges u->v where v==node_id)."""
        if not self.graph.is_directed:
            # For undirected graphs predecessors == successors
            return self.get_successors(node_id)
        return [edge.u.identifier for edge in self.graph.rev_adj.get(node_id, [])]

    def get_neighbors(self, node_id):
        """Return list of neighbor node ids (ignoring orientation)."""
        neighbors = set(self.get_successors(node_id))
        if self.graph.is_directed:
            neighbors.update(self.get_predecessors(node_id))
        return list(neighbors)

    def incident_edges(self, node_id):
        """Return list of incident Edge objects for the given node id."""
        edges = list(self.graph.adj.get(node_id, []))
        # If reverse adjacency exists, include those as well
        if hasattr(self.graph, 'rev_adj'):
            edges += list(self.graph.rev_adj.get(node_id, []))
        return edges

    def out_degree(self, node_id):
        return len(self.graph.adj.get(node_id, []))

    def in_degree(self, node_id):
        if not self.graph.is_directed:
            return self.out_degree(node_id)
        return len(self.graph.rev_adj.get(node_id, []))

    def degree(self, node_id):
        if self.graph.is_directed:
            return self.in_degree(node_id) + self.out_degree(node_id)
        return self.out_degree(node_id)
    
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
        real_nodes = self._real_node_ids()
        
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
        real_nodes = self._real_node_ids()
        num_nodes = len(real_nodes)
        if num_nodes == 0 or num_nodes == 1:
            return True

        # A complete graph must be undirected and simple
        if self.graph.is_directed or self.graph.has_loops or self.graph.has_multiple_edges:
            return False

        # Build unordered edge set between real nodes (frozenset of two node ids)
        edge_set = set()
        for e in self.graph.edges:
            u_id = e.u.identifier
            v_id = e.v.identifier
            if u_id == v_id:
                continue
            if u_id in real_nodes and v_id in real_nodes:
                edge_set.add(frozenset((u_id, v_id)))

        expected_edges = num_nodes * (num_nodes - 1) // 2
        if len(edge_set) != expected_edges:
            return False

        # Verify every unordered pair is present
        real_list = list(real_nodes)
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if frozenset((real_list[i], real_list[j])) not in edge_set:
                    return False
        return True
    
    def is_regular_graph(self):
        """Zjistí, zda je graf regulární (všechny uzly mají stejný stupeň)."""
        real_nodes = self._real_node_ids()
        if not real_nodes:
            return True

        if self.graph.is_directed:
            # Pro orientované grafy: k-regulární znamená stejný in-degree a out-degree pro všechny uzly
            in_degrees = []
            out_degrees = []
            for node_id in real_nodes:
                in_degree = len([e for e in self.graph.rev_adj.get(node_id, []) if e.u.identifier in real_nodes])
                out_degree = len([e for e in self.graph.adj.get(node_id, []) if e.v.identifier in real_nodes])
                in_degrees.append(in_degree)
                out_degrees.append(out_degree)
            
            if not in_degrees or not out_degrees:
                return True
            
            # Všechny uzly musí mít stejný vstupní stupeň a stejný výstupní stupeň
            first_in_degree = in_degrees[0]
            first_out_degree = out_degrees[0]
            return (all(d == first_in_degree for d in in_degrees) and 
                    all(d == first_out_degree for d in out_degrees))
        else:
            # Pro neorientované grafy: všechny uzly mají stejný stupeň
            degrees = []
            for node_id in real_nodes:
                degrees.append(len([e for e in self.graph.adj.get(node_id, []) if e.v.identifier in real_nodes]))

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

    def is_planar_graph(self):
        """
        Heuristická kontrola rovinnosti grafu.

        Poznámka: úplné testování rovinnosti (Hopcroft-Tarjan) je složitější.
        Tato metoda používá nutné podmínky pro jednoduché grafy:
          - pokud m > 3n - 6 -> NENÍ rovinný
          - pokud je bipartitní a m > 2n - 4 -> NENÍ rovinný
        Pokud tyto podmínky nejsou porušeny, metoda vrací True ("pravděpodobně rovinný").

        Vrací False pokud není rovinný podle těchto nutných podmínek.
        """
        real_nodes = self._real_node_ids()
        n = len(real_nodes)
        if n < 3:
            return True

        # Počítáme unikátní neorientované hrany mezi skutečnými uzly (bez smyček)
        edge_set = set()
        for e in self.graph.edges:
            u_id = e.u.identifier
            v_id = e.v.identifier
            if u_id == v_id:
                continue
            if u_id in real_nodes and v_id in real_nodes:
                edge_set.add(frozenset((u_id, v_id)))

        m = len(edge_set)

        # Pokud překračuje horní mez pro jednoduchý graf, není rovinný
        if m > 3 * n - 6:
            return False

        # Pro bipartitní grafy platí přísnější mez
        if self.is_bipartite_graph() and m > 2 * n - 4:
            return False

        # Jinak považujeme graf za pravděpodobně rovinný (heuristika)
        return True
    
    def count_components(self):
        """Spočítá počet komponent grafu."""
        if not self.graph.nodes:
            return 0
        
        real_nodes = self._real_node_ids()
        
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
        # Only consider real nodes for cycle detection
        real_nodes = self._real_node_ids()
        color = {node_id: WHITE for node_id in real_nodes}

        def dfs(node_id):
            if color[node_id] == GRAY:
                return True  # Back edge found, cycle detected
            if color[node_id] == BLACK:
                return False

            color[node_id] = GRAY
            for edge in self.graph.adj.get(node_id, []):
                neigh = edge.v.identifier
                if neigh in color and dfs(neigh):
                    return True
            color[node_id] = BLACK
            return False

        for node_id in list(color.keys()):
            if color[node_id] == WHITE and dfs(node_id):
                return True
        return False
    
    def _has_cycles_undirected(self):
        """Detekce cyklů v neorientovaném grafu pomocí DFS."""
        visited = set()
        real_nodes = self._real_node_ids()

        def dfs(node_id, parent_id):
            visited.add(node_id)
            for edge in self.graph.adj.get(node_id, []):
                neighbor_id = edge.v.identifier
                if neighbor_id not in real_nodes:
                    continue
                if neighbor_id not in visited:
                    if dfs(neighbor_id, node_id):
                        return True
                elif neighbor_id != parent_id:
                    return True
            return False

        for node_id in real_nodes:
            if node_id not in visited:
                if dfs(node_id, None):
                    return True
        return False
    
    def is_tree(self):
        """Zjistí, zda je graf strom (ignoruje placeholder uzly)."""
        real_nodes = self._real_node_ids()
        
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
        
        real_nodes = self._real_node_ids()
        
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
