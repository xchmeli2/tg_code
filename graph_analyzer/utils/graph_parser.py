"""
Parser pro načítání grafů z textových souborů.
"""

from ..models import Node, Edge

class GraphParser:
    """
    Třída pro parsování grafů z textového formátu.
    """
    
    @staticmethod
    def parse_file(file_path):
        """
        Načte graf z textového souboru.
        
        Args:
            file_path (str): Cesta k souboru
            
        Returns:
            tuple: (nodes_dict, edges_list) kde nodes_dict je slovník uzlů a edges_list je seznam hran
            
        Raises:
            FileNotFoundError: Pokud soubor neexistuje
            ValueError: Pokud je formát souboru neplatný
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"Soubor '{file_path}' nebyl nalezen.")
        
        return GraphParser.parse_lines(lines)
    
    @staticmethod
    def parse_lines(lines):
        """
        Parsuje řádky s definicí grafu.
        
        Args:
            lines (list): Seznam řádků s definicí grafu
            
        Returns:
            tuple: (nodes_dict, edges_list)
        """
        nodes_dict = {}
        edges_list = []
        position_counter = 0

        has_asterisks = any('*' in line for line in lines 
            if line.strip() and line.strip().startswith('u '))
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):  # Prázdné řádky a komentáře
                continue
            
            try:
                parts = line.split(';', 1)
                command = parts[0].strip()
                
                if command.startswith('u '):
                    if has_asterisks:
                        node = GraphParser._parse_node_with_position(command, position_counter)
                        position_counter += 1
                    else:
                        node = GraphParser._parse_node(command)
                
                    nodes_dict[node.identifier] = node
                    
                elif command.startswith('h '):
                    edge = GraphParser._parse_edge(command, nodes_dict)
                    if edge:
                        edges_list.append(edge)
                        
            except Exception as e:
                print(f"Varování: Chyba na řádku {line_num}: {e}")
                continue
        
        # Automatické vytvoření hran pro binární strom
        if has_asterisks:
            # Vytvoř level-order sekvenci uzlů  
            node_sequence = []
            temp_position = 0
            
            for line in lines:
                line = line.strip()
                if line.startswith('u '):
                    node_spec = line[2:].split(';')[0].strip()
                    if node_spec == '*':
                        node_sequence.append(f"*_{temp_position}")
                    else:
                        node_sequence.append(node_spec)
                    temp_position += 1
            
            # Vytvoř hrany podle binární struktury
            for i, parent_id in enumerate(node_sequence):
                left_child_idx = 2 * i + 1
                right_child_idx = 2 * i + 2
                
                # Levé dítě
                if left_child_idx < len(node_sequence):
                    child_id = node_sequence[left_child_idx] 
                    if (not parent_id.startswith('*_') and 
                        not child_id.startswith('*_')):
                        from ..models import Edge
                        parent_node = nodes_dict[parent_id]
                        child_node = nodes_dict[child_id]
                        edge = Edge(parent_node, child_node, '>', None, 'left')
                        edges_list.append(edge)
                
                # Pravé dítě  
                if right_child_idx < len(node_sequence):
                    child_id = node_sequence[right_child_idx]
                    if (not parent_id.startswith('*_') and 
                        not child_id.startswith('*_')):
                        from ..models import Edge  
                        parent_node = nodes_dict[parent_id]
                        child_node = nodes_dict[child_id]
                        edge = Edge(parent_node, child_node, '>', None, 'right')
                        edges_list.append(edge)

        return nodes_dict, edges_list
    
    @staticmethod
    def _parse_node(command):
        """
        Parsuje definici uzlu.
        
        Args:
            command (str): Řádek s definicí uzlu
            
        Returns:
            Node: Objekt uzlu
        """
        node_spec = command[2:].strip()
        
        # Formát: u identifier [value] nebo u identifier value nebo u identifier
        if '[' in node_spec and ']' in node_spec:
            # Format: u identifier [value];
            parts = node_spec.split('[', 1)
            identifier = parts[0].strip()
            value_str = parts[1].split(']')[0].strip()
            try:
                value = float(value_str)
            except ValueError:
                value = value_str
        elif ' ' in node_spec:
            # Format: u identifier value; (space-separated)
            parts = node_spec.split(' ', 1)
            identifier = parts[0].strip()
            value_str = parts[1].strip()
            try:
                value = float(value_str)
            except ValueError:
                value = value_str
        else:
            # Format: u identifier; (no value)
            identifier = node_spec.strip()
            value = None
        
        return Node(identifier, value)
    
    @staticmethod
    def _parse_node_with_position(command, position):
        """
        Parsuje uzel s pozičním trackingem pro binární stromy.
        """
        node_spec = command[2:].strip()
        
        if node_spec == '*':
            # Vytvoří unikátní identifikátor pro placeholder uzel
            identifier = f"*_{position}"
            return Node(identifier, None)
        else:
            # Standardní zpracování skutečných uzlů
            return GraphParser._parse_node(command)

    
    @staticmethod
    def _parse_edge(command, nodes_dict):
        """
        Parsuje definici hrany.
        
        Args:
            command (str): Řádek s definicí hrany
            nodes_dict (dict): Slovník existujících uzlů
            
        Returns:
            Edge: Objekt hrany nebo None při chybě
        """
        edge_spec = command[2:].strip()
        
        # Split by spaces, but be careful with weight and label
        parts = edge_spec.split()
        if len(parts) < 3:
            print(f"Varování: Neplatný formát hrany: {edge_spec}")
            return None
        
        u_id = parts[0].strip()
        direction_symbol = parts[1].strip()
        v_id = parts[2].strip()

        u_node = nodes_dict.get(u_id)
        v_node = nodes_dict.get(v_id)

        if not u_node or not v_node:
            print(f"Varování: Uzel(y) pro hranu {u_id} {direction_symbol} {v_id} nebyly nalezeny. Přeskakuji hranu.")
            return None

        weight = None
        label = None

        # Process remaining parts for weight and label
        if len(parts) > 3:
            remaining = ' '.join(parts[3:])
            
            # Check for label first (starts with :)
            if ':' in remaining:
                weight_part, label_part = remaining.split(':', 1)
                label = label_part.strip()
                weight_part = weight_part.strip()
            else:
                weight_part = remaining.strip()
            
            # Try to parse weight
            if weight_part:
                # Remove brackets if present
                weight_str = weight_part.strip('[]')
                if weight_str:
                    try:
                        weight = float(weight_str)
                    except ValueError:
                        # If it's not a number, it might be a string weight
                        weight = weight_str

        # Determine direction for internal representation
        if direction_symbol == '>':
            direction = '>'
        elif direction_symbol == '<':
            direction = '<'
        else:  # '-'
            direction = '-'

        return Edge(u_node, v_node, direction, weight, label)
