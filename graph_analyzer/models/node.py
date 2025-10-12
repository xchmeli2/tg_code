class Node:
    """
    Třída reprezentující uzel v grafu.
    
    Attributes:
        identifier (str): Unikátní identifikátor uzlu
        value: Volitelné ohodnocení uzlu (může být číslo nebo řetězec)
    """
    
    def __init__(self, identifier, value=None):
        """
        Inicializace uzlu.
        
        Args:
            identifier (str): Unikátní identifikátor uzlu
            value: Volitelné ohodnocení uzlu
        """
        self.identifier = identifier
        self.value = value

    def __repr__(self):
        """Řetězcová reprezentace uzlu pro debugging."""
        return f"Node('{self.identifier}', value={self.value})"

    def __eq__(self, other):
        """Porovnání dvou uzlů na základě identifikátoru."""
        if not isinstance(other, Node):
            return NotImplemented
        return self.identifier == other.identifier

    def __hash__(self):
        """Hash funkce pro použití uzlu jako klíče ve slovníku."""
        return hash(self.identifier)
    
    def to_dict(self):
        """
        Převede uzel na slovník pro serializaci.
        
        Returns:
            dict: Slovník s daty uzlu
        """
        return {
            'identifier': self.identifier,
            'value': self.value
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Vytvoří uzel ze slovníku.
        
        Args:
            data (dict): Slovník s daty uzlu
            
        Returns:
            Node: Nový objekt uzlu
        """
        return cls(data['identifier'], data.get('value'))
