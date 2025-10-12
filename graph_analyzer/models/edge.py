from .node import Node

class Edge:
    """
    Třída reprezentující hranu v grafu.
    
    Attributes:
        u (Node): Počáteční uzel hrany
        v (Node): Koncový uzel hrany
        direction (str): Směr hrany ('<', '-', '>')
        weight: Volitelné ohodnocení hrany
        label (str): Volitelné označení hrany
    """
    
    def __init__(self, u, v, direction, weight=None, label=None):
        """
        Inicializace hrany.
        
        Args:
            u (Node): Počáteční uzel
            v (Node): Koncový uzel
            direction (str): Směr hrany ('<', '-', '>')
            weight: Volitelné ohodnocení hrany
            label (str): Volitelné označení hrany
        """
        self.u = u
        self.v = v
        self.direction = direction
        self.weight = weight
        self.label = label

    def __repr__(self):
        """Řetězcová reprezentace hrany pro debugging."""
        if self.direction == '>':
            return f"Edge({self.u.identifier} -> {self.v.identifier}, weight={self.weight}, label='{self.label}')"
        elif self.direction == '<':
            return f"Edge({self.u.identifier} <- {self.v.identifier}, weight={self.weight}, label='{self.label}')"
        else:
            return f"Edge({self.u.identifier} - {self.v.identifier}, weight={self.weight}, label='{self.label}')"

    def __eq__(self, other):
        """Porovnání dvou hran."""
        if not isinstance(other, Edge):
            return NotImplemented
        # Pro neorientované hrany je (u,v) stejné jako (v,u)
        if self.direction == '-' and other.direction == '-':
            return (self.u == other.u and self.v == other.v) or \
                   (self.u == other.v and self.v == other.u)
        return self.u == other.u and self.v == other.v and self.direction == other.direction

    def __hash__(self):
        """Hash funkce pro použití hrany jako klíče ve slovníku."""
        if self.direction == '-':
            return hash(frozenset({self.u, self.v}))
        return hash((self.u, self.v, self.direction))
    
    def is_directed(self):
        """
        Zjistí, zda je hrana orientovaná.
        
        Returns:
            bool: True pro orientované hrany, False pro neorientované
        """
        return self.direction != '-'
    
    def is_loop(self):
        """
        Zjistí, zda je hrana smyčka.
        
        Returns:
            bool: True pokud je hrana smyčka
        """
        return self.u == self.v
    
    def get_other_node(self, node):
        """
        Vrátí druhý uzel hrany (opačný k zadanému).
        
        Args:
            node (Node): Jeden z uzlů hrany
            
        Returns:
            Node: Druhý uzel hrany nebo None pokud zadaný uzel není součástí hrany
        """
        if self.u == node:
            return self.v
        elif self.v == node:
            return self.u
        return None
    
    def to_dict(self):
        """
        Převede hranu na slovník pro serializaci.
        
        Returns:
            dict: Slovník s daty hrany
        """
        return {
            'u_identifier': self.u.identifier,
            'v_identifier': self.v.identifier,
            'direction': self.direction,
            'weight': self.weight,
            'label': self.label
        }
    
    @classmethod
    def from_dict(cls, data, nodes_dict):
        """
        Vytvoří hranu ze slovníku.
        
        Args:
            data (dict): Slovník s daty hrany
            nodes_dict (dict): Slovník uzlů pro nalezení objektů Node
            
        Returns:
            Edge: Nový objekt hrany
        """
        u = nodes_dict[data['u_identifier']]
        v = nodes_dict[data['v_identifier']]
        return cls(u, v, data['direction'], data.get('weight'), data.get('label'))
