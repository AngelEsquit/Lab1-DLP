# Laboratorio 2 - Minimización de AFD

## Descripción

Implementación del algoritmo de minimización de Autómatas Finitos Deterministas (AFD) para obtener un AFD equivalente con el número mínimo de estados posibles. El programa construye un AFD a partir de una expresión regular usando el método directo, luego lo minimiza y compara los resultados.

## Características

- Conversión directa de expresión regular a AFD (sin pasar por AFN)
- Soporte para todos los operadores requeridos: `|` (unión), concatenación (implícita), `*` (Kleene), `+` (positivo), `?` (opcional)
- Generación de tabla de transición de estados
- Simulación del AFD para validar cadenas
- Visualización del recorrido paso a paso
- Sin uso de librerías de expresiones regulares

## Requisitos

- Python 3.6 o superior

## Uso

### Ejecutar el programa

```bash
python3 regex_to_dfa.py
```

### Ejecutar la demo automática (recomendado para el video)

```bash
python3 demo.py
```

### Operadores soportados

- `|` - Unión (OR): `a|b` acepta 'a' o 'b'
- Concatenación: `ab` acepta 'a' seguido de 'b'
- `*` - Cerradura de Kleene: `a*` acepta '', 'a', 'aa', 'aaa', ...
- `+` - Cerradura positiva: `a+` acepta 'a', 'aa', 'aaa', ... (al menos una)
- `?` - Opcional: `a?` acepta '' o 'a'
- `()` - Agrupación: `(ab)*` acepta '', 'ab', 'abab', ...

### Ejemplos de uso

#### Ejemplo 1: Números enteros con signo opcional

**Expresión regular:** `(+|-)?0|1|2|3|4|5|6|7|8|9+`

Esta expresión acepta números como:
- Acepta: `123`, `+456`, `-789`, `0`
- Rechaza: ``, `+`, `-`, `abc`

#### Ejemplo 2: Identificadores en programación

**Expresión regular:** `(a|b|c|d|e)(a|b|c|d|e|0|1|2|3|4)*`

Esta expresión acepta identificadores que comienzan con letra:
- Acepta: `a`, `abc`, `a1b2`, `variable123`
- Rechaza: ``, `1abc`, `123`

#### Ejemplo 3: Cadenas con 'ab' repetido

**Expresión regular:** `(ab)+`

Esta expresión acepta una o más repeticiones de 'ab':
- Acepta: `ab`, `abab`, `ababab`
- Rechaza: ``, `a`, `b`, `aba`, `ba`

## Algoritmo del Método Directo

### Paso 1: Construcción del árbol sintáctico

El parser convierte la expresión regular en un árbol sintáctico donde:
- Los nodos hoja son símbolos del alfabeto
- Los nodos internos son operadores

### Paso 2: Cálculo de funciones

Para cada nodo del árbol se calculan:

- **nullable**: ¿el nodo puede generar la cadena vacía?
- **firstpos**: conjunto de posiciones que pueden aparecer primero
- **lastpos**: conjunto de posiciones que pueden aparecer al final

### Paso 3: Cálculo de followpos

Para cada posición, se calcula qué posiciones pueden seguirla.

### Paso 4: Construcción del AFD

Se construyen los estados del AFD:
- Estado inicial: `firstpos` de la raíz
- Para cada estado y símbolo, se calcula el siguiente estado usando `followpos`
- Estados de aceptación: los que contienen la posición del símbolo `#`

### Paso 5: Simulación

Para validar una cadena, se parte del estado inicial y se siguen las transiciones según cada símbolo de la cadena. Si al terminar se está en un estado de aceptación, la cadena es aceptada.

## Estructura del código

```
regex_to_dfa.py
├── Node                 # Clase para nodos del árbol sintáctico
├── RegexParser          # Parser de expresiones regulares
├── DFABuilder          # Constructor del AFD (método directo)
├── DFASimulator        # Simulador del AFD
└── main()              # Programa principal
```

## Ejemplos para el video de demostración (Lab2)

Para cumplir la rúbrica del laboratorio se muestran dos casos:

### Expresión 1 (AFD ya mínimo): `a|b`
- Acepta: `a`, `b`
- Rechaza: `ab`, `ba`, ``

### Expresión 2 (AFD se reduce): `(a|aa)*`
- Acepta: ``, `a`, `aa`, `aaa`
- Rechaza: `b`, `ab`, `ba`

En el primer caso, el AFD minimizado no cambia.
En el segundo caso, la minimización reduce estados y transiciones.

## Video de Demostración

Puedes ver el video de demostración del programa en el siguiente enlace:
[Demostración en YouTube](https://youtu.be/CwewtK9koVA)

## Branch del laboratorio

Código de la entrega de Lab2 en GitHub:
[Branch Lab2](https://github.com/AngelEsquit/Lab1-DLP/tree/Lab2)

## Notas importantes

- No se utilizan librerías de expresiones regulares
- La implementación es completamente manual