"""
Analyzátor pro cesty a vzdálenosti v grafu.
"""

import heapq
from collections import deque
from typing import Dict, List, Tuple, Optional, Mapping

class PathAnalyzer:
    """
    Třída pro analýzu cest a vzdáleností v grafu.
    """
    
    def __init__(self, graph):
        """
        Inicializace analyzátoru.
        
        Args:
            graph (Graph): Graf k analýze
        """
        self.graph = graph
    
    def find_shortest_path(self, start_id, end_id):
        """
        Najde nejkratší cestu mezi dvěma uzly.
        
        Args:
            start_id (str): Identifikátor počátečního uzlu
            end_id (str): Identifikátor cílového uzlu
            
        Returns:
            list: Seznam identifikátorů uzlů na nejkratší cestě nebo None
        """
        if start_id not in self.graph.nodes or end_id not in self.graph.nodes:
            return None
        
        if not self.graph.is_weighted:
            return self._bfs_shortest_path(start_id, end_id)
        else:
            return self._dijkstra_shortest_path(start_id, end_id)
    
    def _bfs_shortest_path(self, start_id, end_id):
        """BFS pro neohodnocené grafy."""
        queue = deque([(start_id, [start_id])])
        visited = {start_id}
        
        while queue:
            current_id, path = queue.popleft()
            
            if current_id == end_id:
                return path
            
            for edge in self.graph.adj[current_id]:
                next_id = edge.v.identifier
                if next_id not in visited:
                    visited.add(next_id)
                    queue.append((next_id, path + [next_id]))
        
        return None
    
    def _dijkstra_shortest_path(self, start_id, end_id):
        """Dijkstra algoritmus pro ohodnocené grafy."""
        distances = {node_id: float('inf') for node_id in self.graph.nodes}
        distances[start_id] = 0
        previous = {}
        # Use float for distances in the priority queue to satisfy type checkers
        pq: List[Tuple[float, str]] = [(0.0, start_id)]
        
        while pq:
            current_dist, current_id = heapq.heappop(pq)
            
            if current_id == end_id:
                # Reconstruct path
                path = []
                while current_id is not None:
                    path.append(current_id)
                    current_id = previous.get(current_id)
                return path[::-1]
            
            if current_dist > distances[current_id]:
                continue
            
            for edge in self.graph.adj[current_id]:
                next_id = edge.v.identifier
                weight = edge.weight if edge.weight is not None else 1
                if isinstance(weight, (int, float)):
                    distance = current_dist + weight
                    
                    if distance < distances[next_id]:
                        distances[next_id] = distance
                        previous[next_id] = current_id
                        heapq.heappush(pq, (distance, next_id))
        
        return None
    
    def find_all_paths(self, start_id, end_id, max_length=None):
        """
        Najde všechny jednoduché cesty mezi dvěma uzly.
        
        Args:
            start_id (str): Identifikátor počátečního uzlu
            end_id (str): Identifikátor cílového uzlu
            max_length (int): Maximální délka cesty
            
        Returns:
            list: Seznam všech cest (každá cesta je seznam identifikátorů uzlů)
        """
        if start_id not in self.graph.nodes or end_id not in self.graph.nodes:
            return []
        
        paths = []
        
        def dfs(current_id, target_id, path, visited):
            if max_length and len(path) > max_length:
                return
            
            if current_id == target_id:
                paths.append(path[:])
                return
            
            for edge in self.graph.adj[current_id]:
                next_id = edge.v.identifier
                if next_id not in visited:
                    visited.add(next_id)
                    path.append(next_id)
                    dfs(next_id, target_id, path, visited)
                    path.pop()
                    visited.remove(next_id)
        
        visited = {start_id}
        dfs(start_id, end_id, [start_id], visited)
        return paths
    
    def get_shortest_distances(self, start_id):
        """
        Najde nejkratší vzdálenosti od daného uzlu ke všem ostatním uzlům.
        
        Args:
            start_id (str): Identifikátor počátečního uzlu
            
        Returns:
            dict: Slovník vzdáleností {node_id: distance}
        """
        if start_id not in self.graph.nodes:
            return {}
        
        if not self.graph.is_weighted:
            return self._bfs_distances(start_id)
        else:
            return self._dijkstra_distances(start_id)
    
    def _bfs_distances(self, start_id):
        """BFS pro výpočet vzdáleností v neohodnoceném grafu."""
        distances = {start_id: 0}
        queue = deque([start_id])
        
        while queue:
            current_id = queue.popleft()
            
            for edge in self.graph.adj[current_id]:
                next_id = edge.v.identifier
                if next_id not in distances:
                    distances[next_id] = distances[current_id] + 1
                    queue.append(next_id)
        
        return distances
    
    def _dijkstra_distances(self, start_id):
        """Dijkstra pro výpočet vzdáleností v ohodnoceném grafu."""
        distances = {node_id: float('inf') for node_id in self.graph.nodes}
        distances[start_id] = 0
        # Use float distances in the priority queue
        pq: List[Tuple[float, str]] = [(0.0, start_id)]
        
        while pq:
            current_dist, current_id = heapq.heappop(pq)
            
            if current_dist > distances[current_id]:
                continue
            
            for edge in self.graph.adj[current_id]:
                next_id = edge.v.identifier
                weight = edge.weight if edge.weight is not None else 1
                if isinstance(weight, (int, float)):
                    distance = current_dist + weight
                    
                    if distance < distances[next_id]:
                        distances[next_id] = distance
                        heapq.heappush(pq, (distance, next_id))
        
        return distances
    
    def get_node_eccentricity(self, node_id) -> float:
        """
        Vypočítá excentricitu uzlu (maximální vzdálenost k jakémukoli jinému uzlu).
        
        Args:
            node_id (str): Identifikátor uzlu
            
        Returns:
            float: Excentricita uzlu nebo float('inf') pokud graf není souvislý
        """
        if node_id not in self.graph.nodes:
            # For consistency return infinity when node is not present
            return float('inf')

        distances: Mapping[str, float | int] = self.get_shortest_distances(node_id)
        max_distance: float = 0.0

        for other_id in self.graph.nodes:
            if other_id != node_id:
                if other_id in distances:
                    d = distances[other_id]
                    # ensure d is a float (distance functions use numeric values)
                    if d is None:
                        return float('inf')
                    max_distance = max(max_distance, float(d))
                else:
                    return float('inf')  # Not connected

        return max_distance
    
    def get_graph_diameter(self):
        """
        Vypočítá průměr grafu (maximální excentricita).
        
        Returns:
            float: Průměr grafu
        """
        max_eccentricity = 0.0
        for node_id in self.graph.nodes:
            eccentricity = self.get_node_eccentricity(node_id)
            if eccentricity == float('inf'):
                return float('inf')
            max_eccentricity = max(max_eccentricity, eccentricity)
        
        return max_eccentricity
    
    def get_graph_radius(self):
        """
        Vypočítá poloměr grafu (minimální excentricita).
        
        Returns:
            float: Poloměr grafu
        """
        min_eccentricity = float('inf')
        for node_id in self.graph.nodes:
            eccentricity = self.get_node_eccentricity(node_id)
            if eccentricity == float('inf'):
                return float('inf')
            min_eccentricity = min(min_eccentricity, eccentricity)
        
        return min_eccentricity
    
    def find_center_nodes(self):
        """
        Najde centrální uzly grafu (uzly s minimální excentricitou).
        
        Returns:
            list: Seznam identifikátorů centrálních uzlů
        """
        radius = self.get_graph_radius()
        if radius == float('inf'):
            return []
        
        center_nodes = []
        for node_id in self.graph.nodes:
            if self.get_node_eccentricity(node_id) == radius:
                center_nodes.append(node_id)
        
        return center_nodes
