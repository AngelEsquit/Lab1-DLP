"""
Laboratorio 2 - Minimización de AFD
Implementación del algoritmo de minimización para obtener un AFD con número mínimo de estados
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
        if not self.regex:
            raise ValueError("La expresión regular no puede estar vacía")
        
        # Agregar el símbolo de fin '#'
        tree = self.parse_union()
        
        if tree is None:
            raise ValueError("Error al parsear la expresión regular")
        
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
            else:
                raise ValueError(f"Falta paréntesis de cierre en posición {self.pos}")
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


class MinimizedDFASimulator:
    """Simulador de AFD minimizado (con estados enteros)."""

    def __init__(self, dfa_min):
        self.dfa = dfa_min

    def simulate(self, string):
        """Simula el AFD minimizado con una cadena de entrada."""
        current_state = self.dfa['initial']
        path = [f"S{current_state}"]

        for symbol in string:
            if symbol not in self.dfa['alphabet']:
                return False, path, f"Símbolo '{symbol}' no está en el alfabeto"

            key = (current_state, symbol)
            if key in self.dfa['transitions']:
                current_state = self.dfa['transitions'][key]
                path.append(f"--{symbol}--> S{current_state}")
            else:
                return False, path, f"No hay transición desde S{current_state} con '{symbol}'"

        accepted = current_state in self.dfa['accepting']
        return accepted, path, None


class DFAMinimizer:
    """Minimizador de AFD usando algoritmo de particionamiento."""

    def __init__(self, dfa):
        self.dfa = dfa
        self.partitions = []

    def _get_partition_index(self, state):
        for i, partition in enumerate(self.partitions):
            if state in partition:
                return i
        return -1

    def _split_partition(self, partition):
        signatures = {}

        for state in partition:
            sig = []

            for symbol in sorted(self.dfa['alphabet']):
                key = (state, symbol)

                if key in self.dfa['transitions']:
                    next_state = self.dfa['transitions'][key]
                    partition_idx = self._get_partition_index(next_state)
                else:
                    partition_idx = -1

                sig.append((symbol, partition_idx))

            sig = tuple(sig)
            if sig not in signatures:
                signatures[sig] = set()
            signatures[sig].add(state)

        return [frozenset(group) for group in signatures.values()]

    def _build_minimized_dfa(self):
        state_to_partition = {}
        for i, partition in enumerate(self.partitions):
            for state in partition:
                state_to_partition[state] = i

        new_states = list(range(len(self.partitions)))
        initial_partition = state_to_partition[self.dfa['initial']]

        accepting_partition_indices = set()
        for accepting_state in self.dfa['accepting']:
            accepting_partition_indices.add(state_to_partition[accepting_state])

        new_transitions = {}
        for i, partition in enumerate(self.partitions):
            representative = next(iter(partition))
            for symbol in self.dfa['alphabet']:
                key = (representative, symbol)
                if key in self.dfa['transitions']:
                    next_state = self.dfa['transitions'][key]
                    to_partition = state_to_partition[next_state]
                    new_transitions[(i, symbol)] = to_partition

        return {
            'states': new_states,
            'alphabet': list(self.dfa['alphabet']),
            'transitions': new_transitions,
            'initial': initial_partition,
            'accepting': sorted(list(accepting_partition_indices)),
            'partitions': self.partitions,
        }

    def minimize(self):
        """Minimiza el AFD usando el algoritmo de particionamiento."""
        states = self.dfa['states']
        accepting = frozenset(self.dfa['accepting'])
        non_accepting = frozenset(s for s in states if s not in accepting)

        self.partitions = []
        if non_accepting:
            self.partitions.append(non_accepting)
        if accepting:
            self.partitions.append(accepting)

        changed = True
        while changed:
            changed = False
            new_partitions = []

            for partition in self.partitions:
                sub_partitions = self._split_partition(partition)

                if len(sub_partitions) > 1:
                    changed = True

                new_partitions.extend(sub_partitions)

            self.partitions = new_partitions

        return self._build_minimized_dfa()


def print_transition_table_minimized(dfa_min):
    """Imprime la tabla de transición del AFD minimizado."""
    states = dfa_min['states']
    alphabet = dfa_min['alphabet']
    transitions = dfa_min['transitions']
    
    print("\n" + "="*60)
    print("TABLA DE TRANSICIÓN - AFD MINIMIZADO")
    print("="*60)
    
    # Resumen
    print(f"\nEstados: {len(states)} | Alfabeto: {{{', '.join(alphabet)}}} | "
          f"Aceptación: {len(dfa_min['accepting'])}")
    
    # Encabezado
    header = "Estado".ljust(15) + "| " + " | ".join(sym.ljust(10) for sym in alphabet)
    print("\n" + header)
    print("-" * len(header))
    
    # Filas
    for state in states:
        # Marcar estado inicial y de aceptación
        markers = []
        if state == dfa_min['initial']:
            markers.append('->')
        if state in dfa_min['accepting']:
            markers.append('*')
        
        marker_str = ''.join(markers)
        state_str = f"{marker_str}S{state}".ljust(15)
        
        row = [state_str]
        for symbol in alphabet:
            key = (state, symbol)
            if key in transitions:
                next_state = transitions[key]
                row.append(f"S{next_state}".ljust(10))
            else:
                row.append("-".ljust(10))
        
        print("| ".join(row))
    
    print("\nLeyenda: -> = Estado inicial, * = Estado de aceptación")


def print_transition_table(dfa):
    """Imprime la tabla de transición del AFD original."""
    states = dfa['states']
    alphabet = dfa['alphabet']
    transitions = dfa['transitions']
    
    # Crear mapeo de estados a nombres
    state_names = {}
    for i, state in enumerate(states):
        state_names[state] = f"S{i}"
    
    print("\n" + "="*60)
    print("TABLA DE TRANSICIÓN - AFD ORIGINAL")
    print("="*60)
    
    # Resumen
    print(f"\nEstados: {len(states)} | Alfabeto: {{{', '.join(alphabet)}}} | "
          f"Aceptación: {len(dfa['accepting'])}")
    
    # Encabezado
    header = "Estado".ljust(15) + "| " + " | ".join(sym.ljust(10) for sym in alphabet)
    print("\n" + header)
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
    """Programa principal interactivo."""
    print("="*60)
    print("MINIMIZACIÓN DE AFD - LABORATORIO 2")
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
            
            # 2. Construir el AFD ORIGINAL
            print("\n2. Construyendo AFD (método directo)...")
            builder = DFABuilder(tree, parser.positions)
            dfa_original = builder.build_dfa()
            num_states_original = len(dfa_original['states'])
            num_transitions_original = len(dfa_original['transitions'])
            
            print(f"   ✓ AFD construido con {num_states_original} estados")
            print(f"   ✓ {num_transitions_original} transiciones")
            print(f"   ✓ Alfabeto: {{{', '.join(dfa_original['alphabet'])}}}")
            
            # 3. Mostrar tabla de transición ORIGINAL
            print_transition_table(dfa_original)
            
            # 4. MINIMIZAR el AFD
            print("\n3. Minimizando AFD...")
            minimizer = DFAMinimizer(dfa_original)
            dfa_minimized = minimizer.minimize()
            num_states_minimized = len(dfa_minimized['states'])
            num_transitions_minimized = len(dfa_minimized['transitions'])
            
            print(f"   ✓ AFD minimizado con {num_states_minimized} estados")
            print(f"   ✓ {num_transitions_minimized} transiciones")
            
            # 5. Mostrar tabla de transición MINIMIZADO
            print_transition_table_minimized(dfa_minimized)
            
            # 6. COMPARACIÓN
            print("\n" + "="*60)
            print("COMPARACIÓN DE RESULTADOS")
            print("="*60)
            print(f"\nAFD Original:")
            print(f"  • Estados: {num_states_original}")
            print(f"  • Transiciones: {num_transitions_original}")
            
            print(f"\nAFD Minimizado:")
            print(f"  • Estados: {num_states_minimized}")
            print(f"  • Transiciones: {num_transitions_minimized}")
            
            reduction_states = num_states_original - num_states_minimized
            reduction_transitions = num_transitions_original - num_transitions_minimizado
            
            print(f"\nReducción:")
            print(f"  • Estados reducidos: {reduction_states} ({100*reduction_states/num_states_original:.1f}%)")
            print(f"  • Transiciones reducidas: {reduction_transitions}")
            
            if reduction_states == 0:
                print(f"\n  ℹ El AFD original ya es MÍNIMO (sin cambios)")
            else:
                print(f"\n  ✓ El AFD se minimizó exitosamente")
            
            # 7. Simular con el AFD minimizado
            simulator = MinimizedDFASimulator(dfa_minimized)
            
            while True:
                print("\n" + "-"*60)
                cadena = input("\nIngrese cadena para validar (o 'nuevo' para nueva expresión): ").strip()
                
                if cadena.lower() == 'nuevo':
                    break
                
                if not cadena:
                    cadena_display = "(cadena vacía)"
                else:
                    cadena_display = cadena
                
                print(f"\nValidando: '{cadena_display}'")
                print("-" * 40)
                
                accepted, path, error = simulator.simulate(cadena)
                
                print("Recorrido:")
                for step in path:
                    print(f"  {step}")
                
                if error:
                    print(f"\n✗ {error}")
                elif accepted:
                    print(f"\n✓ ACEPTADA - Pertenece al lenguaje")
                else:
                    print(f"\n✗ RECHAZADA - No pertenece al lenguaje")
        
        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
