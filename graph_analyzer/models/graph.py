import collections
from .node import Node
from .edge import Edge

class Graph:
    """
    Třída reprezentující graf s jeho základními vlastnostmi a operacemi.
    """
    
    def __init__(self):
        """Inicializace prázdného grafu."""
        self.nodes = {}
        self.adj = collections.defaultdict(list)  # Adjacency list for outgoing edges
        self.rev_adj = collections.defaultdict(list)  # Adjacency list for incoming edges (for directed graphs)
        self.edges = []
        self.is_directed = False
        self.is_weighted = False
        self.has_loops = False
        self.has_multiple_edges = False

    def add_node(self, node):
        """
        Přidá uzel do grafu.
        
        Args:
            node (Node): Uzel k přidání
        """
        if node.identifier not in self.nodes:
            self.nodes[node.identifier] = node

    def add_edge(self, edge):
        """
        Přidá hranu do grafu.
        
        Args:
            edge (Edge): Hrana k přidání
        """
        # Check if nodes exist, if not, add them
        if edge.u.identifier not in self.nodes:
            self.add_node(edge.u)
        if edge.v.identifier not in self.nodes:
            self.add_node(edge.v)

        # Update graph properties
        if edge.direction != '-':
            self.is_directed = True
        if edge.weight is not None:
            self.is_weighted = True
        if edge.u == edge.v:
            self.has_loops = True

        # Check for multiple edges
        for existing_edge in self.adj[edge.u.identifier]:
            if existing_edge.v == edge.v and existing_edge.direction == edge.direction:
                self.has_multiple_edges = True
                break
        if not self.is_directed:
            for existing_edge in self.adj[edge.v.identifier]:
                if existing_edge.v == edge.u and existing_edge.direction == edge.direction:
                    self.has_multiple_edges = True
                    break

        self.edges.append(edge)
        
        # Handle adjacency lists based on edge direction
        if edge.direction == '>':
            # u -> v: u has outgoing edge to v, v has incoming edge from u
            self.adj[edge.u.identifier].append(edge)
            self.rev_adj[edge.v.identifier].append(edge)
        elif edge.direction == '<':
            # u <- v: v has outgoing edge to u, u has incoming edge from v
            actual_edge = Edge(edge.v, edge.u, '>', edge.weight, edge.label)
            self.adj[edge.v.identifier].append(actual_edge)
            self.rev_adj[edge.u.identifier].append(actual_edge)
        else:  # '-' undirected
            # For undirected, both nodes can reach each other
            self.adj[edge.u.identifier].append(edge)
            reverse_edge = Edge(edge.v, edge.u, '-', edge.weight, edge.label)
            self.adj[edge.v.identifier].append(reverse_edge)

    def load_from_data(self, nodes_dict, edges_list):
        """
        Načte graf z parsovaných dat.
        
        Args:
            nodes_dict (dict): Slovník uzlů
            edges_list (list): Seznam hran
        """
        # Reset graph
        self.__init__()
        
        # Add nodes
        for node in nodes_dict.values():
            self.add_node(node)
        
        # Add edges
        for edge in edges_list:
            self.add_edge(edge)

    def get_node_count(self):
        """Vrátí počet uzlů v grafu."""
        return len(self.nodes)

    def get_edge_count(self):
        """Vrátí počet hran v grafu."""
        return len(self.edges)

    def get_node(self, identifier):
        """
        Vrátí uzel podle identifikátoru.
        
        Args:
            identifier (str): Identifikátor uzlu
            
        Returns:
            Node: Uzel nebo None pokud neexistuje
        """
        return self.nodes.get(identifier)

    def has_node(self, identifier):
        """
        Zjistí, zda graf obsahuje uzel s daným identifikátorem.
        
        Args:
            identifier (str): Identifikátor uzlu
            
        Returns:
            bool: True pokud uzel existuje
        """
        return identifier in self.nodes

    def get_neighbors(self, node_id):
        """
        Vrátí seznam sousedů uzlu.
        
        Args:
            node_id (str): Identifikátor uzlu
            
        Returns:
            list: Seznam identifikátorů sousedních uzlů
        """
        if node_id not in self.nodes:
            return None
        
        neighbors = set()
        for edge in self.adj[node_id]:
            neighbors.add(edge.v.identifier)
        
        # For directed graphs, also check reverse adjacency
        if self.is_directed:
            for edge in self.rev_adj[node_id]:
                neighbors.add(edge.u.identifier)
        
        return list(neighbors)

    def get_successors(self, node_id):
        """
        Vrátí seznam následníků uzlu (pro orientované grafy).
        
        Args:
            node_id (str): Identifikátor uzlu
            
        Returns:
            list: Seznam identifikátorů následníků
        """
        if node_id not in self.nodes:
            return None
        return [edge.v.identifier for edge in self.adj[node_id] if edge.direction == '>']

    def get_predecessors(self, node_id):
        """
        Vrátí seznam předchůdců uzlu (pro orientované grafy).
        
        Args:
            node_id (str): Identifikátor uzlu
            
        Returns:
            list: Seznam identifikátorů předchůdců
        """
        if node_id not in self.nodes:
            return None
        return [edge.u.identifier for edge in self.rev_adj[node_id] if edge.direction == '>']

    def get_node_degree(self, node_id):
        """
        Vrátí informace o stupni uzlu.
        
        Args:
            node_id (str): Identifikátor uzlu
            
        Returns:
            dict: Slovník s informacemi o stupni uzlu
        """
        if node_id not in self.nodes:
            return None
        
        if self.is_directed:
            in_degree = len(self.rev_adj[node_id])
            out_degree = len(self.adj[node_id])
            return {
                'in_degree': in_degree,
                'out_degree': out_degree,
                'total_degree': in_degree + out_degree
            }
        else:
            return {'total_degree': len(self.adj[node_id])}

    def is_isolated_node(self, node_id):
        """
        Zjistí, zda je uzel izolovaný.
        
        Args:
            node_id (str): Identifikátor uzlu
            
        Returns:
            bool: True pokud je uzel izolovaný
        """
        if node_id not in self.nodes:
            return None
        
        degree_info = self.get_node_degree(node_id)
        if degree_info is None:
            return None
        if self.is_directed:
            return degree_info['total_degree'] == 0
        else:
            return degree_info['total_degree'] == 0

    def to_dict(self):
        """
        Převede graf na slovník pro serializaci.
        
        Returns:
            dict: Slovník s daty grafu
        """
        return {
            'nodes': [node.to_dict() for node in self.nodes.values()],
            'edges': [edge.to_dict() for edge in self.edges],
            'properties': {
                'is_directed': self.is_directed,
                'is_weighted': self.is_weighted,
                'has_loops': self.has_loops,
                'has_multiple_edges': self.has_multiple_edges
            }
        }
