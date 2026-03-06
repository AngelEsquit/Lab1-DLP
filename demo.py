"""
Script de demostración automática
Ejecuta las tres expresiones regulares con casos de prueba
"""

from regex_to_dfa import RegexParser, DFABuilder, DFASimulator, print_transition_table
import time

def demo_regex(regex_num, regex, test_cases):
    """Demuestra una expresión regular con casos de prueba"""
    print("\n" + "="*80)
    print(f"DEMOSTRACIÓN {regex_num}")
    print("="*80)
    print(f"\nExpresión Regular: {regex}")
    
    try:
        # Parsear y construir AFD
        print("\nConstruyendo AFD...")
        parser = RegexParser(regex)
        tree = parser.parse()
        builder = DFABuilder(tree, parser.positions)
        dfa = builder.build_dfa()
        
        print(f"✓ AFD construido exitosamente")
        print(f"  - Estados: {len(dfa['states'])}")
        print(f"  - Alfabeto: {{{', '.join(dfa['alphabet'])}}}")
        
        # Mostrar tabla de transición
        print_transition_table(dfa)
        
        # Probar cadenas
        simulator = DFASimulator(dfa)
        
        print("\n" + "-"*80)
        print("PRUEBAS DE VALIDACIÓN")
        print("-"*80)
        
        for i, (cadena, should_accept) in enumerate(test_cases, 1):
            cadena_display = cadena if cadena else "(cadena vacía)"
            print(f"\nPrueba {i}: '{cadena_display}'")
            print("-" * 40)
            
            accepted, path, error = simulator.simulate(cadena)
            
            print("Recorrido del AFD:")
            for step in path:
                print(f"  {step}")
            
            if error:
                print(f"\n✗ RECHAZADA: {error}")
            elif accepted:
                print(f"\n✓ ACEPTADA - La cadena pertenece al lenguaje")
            else:
                print(f"\n✗ RECHAZADA - La cadena NO pertenece al lenguaje")
            
            # Verificar si el resultado es el esperado
            if accepted == should_accept:
                print(f"   [Resultado correcto: {'ACEPTA' if should_accept else 'RECHAZA'}]")
            else:
                print(f"   [ERROR: Se esperaba {'ACEPTAR' if should_accept else 'RECHAZAR'}]")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Ejecuta las tres demostraciones"""
    print("="*80)
    print("DEMOSTRACIÓN AUTOMÁTICA - MÉTODO DIRECTO REGEX A AFD")
    print("Laboratorio 01 - Diseño de Lenguajes de Programación")
    print("="*80)
    
    # Expresión 1: a(b|c)*d
    demo_regex(
        1,
        "a(b|c)*d",
        [
            ("abcd", True),    # Acepta: a, luego b y c, termina en d
            ("abc", False),    # Rechaza: falta la d final
            ("ad", True),      # Acepta: a seguido directamente de d (cero repeticiones)
            ("abbbcd", True),  # Acepta: múltiples b's
        ]
    )
    
    input("\n\nPresione Enter para continuar con la siguiente demostración...")
    
    # Expresión 2: (0|1)+
    demo_regex(
        2,
        "(0|1)+",
        [
            ("1010", True),    # Acepta: cadena binaria válida
            ("", False),       # Rechaza: cadena vacía (se necesita al menos un símbolo)
            ("0", True),       # Acepta: un solo símbolo
            ("111000", True),  # Acepta: múltiples símbolos
        ]
    )
    
    input("\n\nPresione Enter para continuar con la siguiente demostración...")
    
    # Expresión 3: x(y)?z+
    demo_regex(
        3,
        "x(y)?z+",
        [
            ("xyz", True),     # Acepta: x, y opcional presente, una z
            ("xy", False),     # Rechaza: falta la z al final
            ("xz", True),     # Acepta: x, y opcional ausente, una z
            ("xyzzzz", True),  # Acepta: x, y, múltiples z's
        ]
    )
    
    print("\n" + "="*80)
    print("DEMOSTRACIÓN COMPLETADA")
    print("="*80)
    print("\nResumen de operadores utilizados:")
    print("  ✓ Unión (|): Expresiones 1 y 2")
    print("  ✓ Concatenación (implícita): Todas las expresiones")
    print("  ✓ Cerradura de Kleene (*): Expresión 1")
    print("  ✓ Cerradura positiva (+): Expresiones 2 y 3")
    print("  ✓ Opcional (?): Expresión 3")
    print("\n¡Todos los operadores requeridos están cubiertos!")


if __name__ == "__main__":
    main()
