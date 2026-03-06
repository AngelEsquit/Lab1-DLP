# Laboratorio 01 - Conversión Directa de Expresión Regular a AFD

## Descripción

Implementación del método directo para construir un Autómata Finito Determinista (AFD) a partir de una expresión regular y simular su funcionamiento.

## Características

- ✅ Conversión directa de expresión regular a AFD (sin pasar por AFN)
- ✅ Soporte para todos los operadores requeridos: `|` (unión), concatenación (implícita), `*` (Kleene), `+` (positivo), `?` (opcional)
- ✅ Generación de tabla de transición de estados
- ✅ Simulación del AFD para validar cadenas
- ✅ Visualización del recorrido paso a paso
- ✅ Sin uso de librerías de expresiones regulares

## Requisitos

- Python 3.6 o superior

## Instalación

No requiere instalación de dependencias adicionales. Solo Python estándar.

## Uso

### Ejecutar el programa

```bash
python regex_to_dfa.py
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
- ✅ Acepta: `123`, `+456`, `-789`, `0`
- ❌ Rechaza: ``, `+`, `-`, `abc`

#### Ejemplo 2: Identificadores en programación

**Expresión regular:** `(a|b|c|d|e)(a|b|c|d|e|0|1|2|3|4)*`

Esta expresión acepta identificadores que comienzan con letra:
- ✅ Acepta: `a`, `abc`, `a1b2`, `variable123`
- ❌ Rechaza: ``, `1abc`, `123`

#### Ejemplo 3: Cadenas con 'ab' repetido

**Expresión regular:** `(ab)+`

Esta expresión acepta una o más repeticiones de 'ab':
- ✅ Acepta: `ab`, `abab`, `ababab`
- ❌ Rechaza: ``, `a`, `b`, `aba`, `ba`

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

## Ejemplos para el video de demostración

### Expresión 1: `a(b|c)*d`

Acepta 'a' seguido de cero o más 'b' o 'c', terminando en 'd'.

- ✅ Acepta: `ad`, `abd`, `acd`, `abcd`, `acbd`, `abbbbcd`
- ❌ Rechaza: ``, `a`, `d`, `ab`, `abc`

### Expresión 2: `(0|1)+`

Acepta una o más ocurrencias de '0' o '1' (números binarios no vacíos).

- ✅ Acepta: `0`, `1`, `01`, `10`, `1010`, `111000`
- ❌ Rechaza: ``, `2`, `012`, `abc`

### Expresión 3: `x(y)?z+`

Acepta 'x', opcionalmente 'y', seguido de una o más 'z'.

- ✅ Acepta: `xz`, `xzz`, `xyz`, `xyzz`, `xyzzz`
- ❌ Rechaza: ``, `x`, `xy`, `xzy`, `yz`

## Validación de operadores

Las tres expresiones anteriores incluyen todos los operadores requeridos:
- ✅ Unión `|`: presente en expresiones 1 y 2  
- ✅ Concatenación: presente en todas
- ✅ Kleene `*`: presente en expresión 1
- ✅ Positivo `+`: presente en expresiones 2 y 3
- ✅ Opcional `?`: presente en expresión 3

## Autores

Laboratorio 01 - Diseño de Lenguajes de Programación

## Notas importantes

- ⚠️ No se utilizan librerías de expresiones regulares
- ⚠️ La implementación es completamente manual
- ⚠️ El video de demostración no debe exceder 5 minutos
- ⚠️ Fecha de entrega: jueves 12 de marzo de 2026, 19:00 horas
