"""
Laboratorio 01 - Conversión directa de una expresión regular a un AFD
Implementación del método directo para construir un AFD a partir de una expresión regular
"""

class Node:
    """Nodo del árbol sintáctico"""
    def __init__(self, tipo, valor=None, izq=None, der=None):
        self.tipo = tipo  # 'symbol', 'concat', 'union', 'star', 'plus', 'optional'
        self.valor = valor
        self.izq = izq
        self.der = der
        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()
        self.position = None  # Para nodos hoja
        
    def __repr__(self):
        if self.tipo == 'symbol':
            return f"Node({self.valor}, pos={self.position})"
        return f"Node({self.tipo})"


class RegexParser:
    """Parser de expresiones regulares"""
    
    def __init__(self, regex):
        self.regex = regex
        self.pos = 0
        self.position_counter = 1
        self.positions = {}  # position -> symbol
        
    def parse(self):
        """Parsea la expresión regular y retorna el árbol sintáctico"""
        # Agregar el símbolo de fin '#'
        tree = self.parse_union()
        end_node = Node('symbol', '#')
        end_node.position = self.position_counter
        self.positions[self.position_counter] = '#'
        self.position_counter += 1
        
        # Concatenar con '#'
        result = Node('concat', izq=tree, der=end_node)
        return result
    
    def parse_union(self):
        """Parsea el operador de unión '|'"""
        left = self.parse_concat()
        
        while self.pos < len(self.regex) and self.regex[self.pos] == '|':
            self.pos += 1
            right = self.parse_concat()
            left = Node('union', izq=left, der=right)
            
        return left
    
    def parse_concat(self):
        """Parsea la concatenación (implícita)"""
        nodes = []
        
        while self.pos < len(self.regex):
            if self.regex[self.pos] in ')|':
                break
            nodes.append(self.parse_postfix())
        
        if not nodes:
            return None
            
        result = nodes[0]
        for node in nodes[1:]:
            result = Node('concat', izq=result, der=node)
            
        return result
    
    def parse_postfix(self):
        """Parsea los operadores postfijos (*, +, ?)"""
        node = self.parse_basic()
        
        while self.pos < len(self.regex):
            if self.regex[self.pos] == '*':
                self.pos += 1
                node = Node('star', izq=node)
            elif self.regex[self.pos] == '+':
                self.pos += 1
                node = Node('plus', izq=node)
            elif self.regex[self.pos] == '?':
                self.pos += 1
                node = Node('optional', izq=node)
            else:
                break
                
        return node
    
    def parse_basic(self):
        """Parsea símbolos básicos y paréntesis"""
        if self.pos >= len(self.regex):
            return None
            
        # Paréntesis
        if self.regex[self.pos] == '(':
            self.pos += 1
            node = self.parse_union()
            if self.pos < len(self.regex) and self.regex[self.pos] == ')':
                self.pos += 1
            return node
        
        # Símbolo normal
        if self.regex[self.pos] not in '()|*+?':
            symbol = self.regex[self.pos]
            self.pos += 1
            node = Node('symbol', symbol)
            node.position = self.position_counter
            self.positions[self.position_counter] = symbol
            self.position_counter += 1
            return node
            
        return None


class DFABuilder:
    """Constructor de AFD usando el método directo"""
    
    def __init__(self, tree, positions):
        self.tree = tree
        self.positions = positions
        self.followpos = {pos: set() for pos in positions.keys()}
        
    def calculate_functions(self, node):
        """Calcula nullable, firstpos y lastpos para todos los nodos"""
        if node is None:
            return
        
        # Recursión
        self.calculate_functions(node.izq)
        self.calculate_functions(node.der)
        
        # Cálculo según el tipo de nodo
        if node.tipo == 'symbol':
            node.nullable = False
            node.firstpos = {node.position}
            node.lastpos = {node.position}
            
        elif node.tipo == 'union':
            node.nullable = node.izq.nullable or node.der.nullable
            node.firstpos = node.izq.firstpos | node.der.firstpos
            node.lastpos = node.izq.lastpos | node.der.lastpos
            
        elif node.tipo == 'concat':
            node.nullable = node.izq.nullable and node.der.nullable
            
            if node.izq.nullable:
                node.firstpos = node.izq.firstpos | node.der.firstpos
            else:
                node.firstpos = node.izq.firstpos
                
            if node.der.nullable:
                node.lastpos = node.izq.lastpos | node.der.lastpos
            else:
                node.lastpos = node.der.lastpos
                
        elif node.tipo == 'star':
            node.nullable = True
            node.firstpos = node.izq.firstpos
            node.lastpos = node.izq.lastpos
            
        elif node.tipo == 'plus':
            node.nullable = node.izq.nullable
            node.firstpos = node.izq.firstpos
            node.lastpos = node.izq.lastpos
            
        elif node.tipo == 'optional':
            node.nullable = True
            node.firstpos = node.izq.firstpos
            node.lastpos = node.izq.lastpos
    
    def calculate_followpos(self, node):
        """Calcula followpos para todos los nodos"""
        if node is None:
            return
        
        if node.tipo == 'concat':
            for pos in node.izq.lastpos:
                self.followpos[pos] |= node.der.firstpos
                
        elif node.tipo in ['star', 'plus']:
            for pos in node.lastpos:
                self.followpos[pos] |= node.firstpos
        
        # Recursión
        self.calculate_followpos(node.izq)
        self.calculate_followpos(node.der)
    
    def build_dfa(self):
        """Construye el AFD"""
        # Calcular las funciones
        self.calculate_functions(self.tree)
        self.calculate_followpos(self.tree)
        
        # Obtener el alfabeto (sin '#')
        alphabet = sorted(set(sym for sym in self.positions.values() if sym != '#'))
        
        # Estado inicial: firstpos del nodo raíz
        initial_state = frozenset(self.tree.firstpos)
        
        # Estados por procesar
        unmarked_states = [initial_state]
        states = [initial_state]
        transitions = {}
        
        # Construir estados y transiciones
        while unmarked_states:
            current = unmarked_states.pop(0)
            
            for symbol in alphabet:
                # Calcular siguiente estado
                next_state = set()
                for pos in current:
                    if self.positions[pos] == symbol:
                        next_state |= self.followpos[pos]
                
                if next_state:
                    next_state = frozenset(next_state)
                    
                    if next_state not in states:
                        states.append(next_state)
                        unmarked_states.append(next_state)
                    
                    transitions[(current, symbol)] = next_state
        
        # Encontrar posición del símbolo '#'
        end_position = None
        for pos, sym in self.positions.items():
            if sym == '#':
                end_position = pos
                break
        
        # Estados de aceptación: los que contienen la posición de '#'
        accepting_states = [s for s in states if end_position in s]
        
        return {
            'states': states,
            'alphabet': alphabet,
            'transitions': transitions,
            'initial': initial_state,
            'accepting': accepting_states
        }


class DFASimulator:
    """Simulador de AFD"""
    
    def __init__(self, dfa):
        self.dfa = dfa
        # Crear mapeo de estados a nombres legibles
        self.state_names = {}
        for i, state in enumerate(dfa['states']):
            self.state_names[state] = f"S{i}"
    
    def simulate(self, string):
        """Simula el AFD con una cadena de entrada"""
        current_state = self.dfa['initial']
        path = [self.state_label(current_state)]
        
        for symbol in string:
            if symbol not in self.dfa['alphabet']:
                return False, path, f"Símbolo '{symbol}' no está en el alfabeto"
            
            key = (current_state, symbol)
            if key in self.dfa['transitions']:
                current_state = self.dfa['transitions'][key]
                path.append(f"--{symbol}--> {self.state_label(current_state)}")
            else:
                return False, path, f"No hay transición desde {self.state_label(current_state)} con '{symbol}'"
        
        accepted = current_state in self.dfa['accepting']
        return accepted, path, None
    
    def state_label(self, state):
        """Retorna el nombre del estado con sus posiciones"""
        name = self.state_names.get(state, '?')
        positions = '{' + ','.join(str(p) for p in sorted(state)) + '}'
        return f"{name} {positions}"
    
    def state_to_string(self, state):
        """Convierte un estado (frozenset) a string legible"""
        return '{' + ','.join(str(p) for p in sorted(state)) + '}'


def print_transition_table(dfa):
    """Imprime la tabla de transición de estados"""
    states = dfa['states']
    alphabet = dfa['alphabet']
    transitions = dfa['transitions']
    
    # Crear mapeo de estados a nombres
    state_names = {}
    for i, state in enumerate(states):
        state_names[state] = f"S{i}"
    
    print("\n" + "="*60)
    print("TABLA DE TRANSICIÓN DE ESTADOS")
    print("="*60)
    
    # Encabezado
    header = "Estado".ljust(15) + "| " + " | ".join(sym.ljust(10) for sym in alphabet)
    print(header)
    print("-" * len(header))
    
    # Filas
    for state in states:
        state_name = state_names[state]
        
        # Marcar estado inicial y de aceptación
        markers = []
        if state == dfa['initial']:
            markers.append('->')
        if state in dfa['accepting']:
            markers.append('*')
        
        marker_str = ''.join(markers)
        state_str = f"{marker_str}{state_name}".ljust(15)
        
        row = [state_str]
        for symbol in alphabet:
            key = (state, symbol)
            if key in transitions:
                next_state = transitions[key]
                row.append(state_names[next_state].ljust(10))
            else:
                row.append("-".ljust(10))
        
        print("| ".join(row))
    
    print("\nLeyenda: -> = Estado inicial, * = Estado de aceptación")
    
    # Mostrar detalles de los estados
    print("\nDetalles de estados:")
    for state in states:
        positions = sorted(state)
        print(f"  {state_names[state]}: {{{','.join(str(p) for p in positions)}}}")


def main():
    """Programa principal"""
    print("="*60)
    print("CONVERSIÓN DIRECTA DE EXPRESIÓN REGULAR A AFD")
    print("Método Directo - Laboratorio 01")
    print("="*60)
    
    while True:
        print("\n" + "-"*60)
        regex = input("\nIngrese una expresión regular (o 'salir' para terminar): ").strip()
        
        if regex.lower() == 'salir':
            print("¡Hasta luego!")
            break
        
        if not regex:
            print("Error: La expresión regular no puede estar vacía")
            continue
        
        try:
            # 1. Parsear la expresión regular
            print("\n1. Parseando expresión regular...")
            parser = RegexParser(regex)
            tree = parser.parse()
            print(f"   ✓ Árbol sintáctico construido")
            print(f"   ✓ Posiciones encontradas: {len(parser.positions)}")
            
            # 2. Construir el AFD
            print("\n2. Construyendo AFD usando método directo...")
            builder = DFABuilder(tree, parser.positions)
            dfa = builder.build_dfa()
            print(f"   ✓ AFD construido con {len(dfa['states'])} estados")
            print(f"   ✓ Alfabeto: {{{', '.join(dfa['alphabet'])}}}")
            
            # 3. Mostrar tabla de transición
            print_transition_table(dfa)
            
            # 4. Simular con cadenas
            simulator = DFASimulator(dfa)
            
            while True:
                print("\n" + "-"*60)
                cadena = input("\nIngrese una cadena para validar (o Enter para nueva expresión): ").strip()
                
                if not cadena:
                    break
                
                print(f"\nValidando cadena: '{cadena}'")
                print("-" * 40)
                
                accepted, path, error = simulator.simulate(cadena)
                
                print("Recorrido:")
                for step in path:
                    print(f"  {step}")
                
                if error:
                    print(f"\n✗ Rechazo: {error}")
                elif accepted:
                    print(f"\n✓ CADENA ACEPTADA - La cadena '{cadena}' pertenece al lenguaje")
                else:
                    print(f"\n✗ CADENA RECHAZADA - La cadena '{cadena}' NO pertenece al lenguaje")
                    print(f"   El estado final no es de aceptación")
        
        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
