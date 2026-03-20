"""
Script de demostración - Laboratorio 2
Demuestra minimización de AFD con dos expresiones regulares
"""

from regex_to_dfa import (
    RegexParser,
    DFABuilder,
    DFAMinimizer,
    print_transition_table,
    print_transition_table_minimized,
    MinimizedDFASimulator,
)


def ejecutar_prueba(simulator, cadena, debe_aceptar):
    cadena_display = cadena if cadena else "(cadena vacía)"
    accepted, path, error = simulator.simulate(cadena)

    print(f"Ingresando: '{cadena_display}'")
    print("Recorrido:")
    for step in path:
        print(f"  {step}")

    if error:
        print(f"\n✗ Error: {error}")
    elif accepted == debe_aceptar:
        print("\n✓ Resultado esperado")
    else:
        print("\n✗ Resultado inesperado")


def demo_minimizacion(demo_num, regex, cadena_valida, cadena_invalida):
    print("\n" + "=" * 80)
    print(f"DEMOSTRACIÓN {demo_num}")
    print("=" * 80)
    print(f"\nExpresión regular: {regex}")

    parser = RegexParser(regex)
    tree = parser.parse()
    builder = DFABuilder(tree, parser.positions)
    dfa_original = builder.build_dfa()

    print("\nAFD ORIGINAL")
    print_transition_table(dfa_original)

    minimizer = DFAMinimizer(dfa_original)
    dfa_min = minimizer.minimize()

    print("\nAFD MINIMIZADO")
    print_transition_table_minimized(dfa_min)

    estados_original = len(dfa_original["states"])
    estados_min = len(dfa_min["states"])
    trans_original = len(dfa_original["transitions"])
    trans_min = len(dfa_min["transitions"])

    print("\n" + "=" * 80)
    print("COMPARACIÓN")
    print("=" * 80)
    print(f"Estados: {estados_original} -> {estados_min}")
    print(f"Transiciones: {trans_original} -> {trans_min}")

    if estados_original == estados_min:
        print("Resultado: el AFD ya era mínimo")
    else:
        print("Resultado: el AFD se redujo")

    simulator = MinimizedDFASimulator(dfa_min)
    print("\nPrueba cadena válida")
    ejecutar_prueba(simulator, cadena_valida, True)

    print("\nPrueba cadena inválida")
    ejecutar_prueba(simulator, cadena_invalida, False)


def main():
    print("=" * 80)
    print("MINIMIZACIÓN DE AFD - LABORATORIO 2")
    print("=" * 80)

    # Caso que no se reduce
    demo_minimizacion(1, "a|b", "a", "ab")

    input("\nPresione Enter para continuar...")

    # Caso que sí se reduce al minimizar
    demo_minimizacion(2, "(a|aa)*", "aa", "b")


if __name__ == "__main__":
    main()
