# Casos de Prueba para el Video de Demostración

## Instrucciones para el Video

Para cada expresión regular:
1. Ingresar la expresión
2. Mostrar la tabla de transición generada
3. Probar una cadena que SÍ pertenece al lenguaje
4. Probar una cadena que NO pertenece al lenguaje

---

## Expresión Regular 1: `a(b|c)*d`

**Descripción:** Acepta la letra 'a', seguida de cero o más 'b' o 'c' (en cualquier orden), terminando con 'd'.

**Operadores utilizados:** 
- Concatenación (implícita)
- Unión `|`
- Cerradura de Kleene `*`

### Cadenas para probar:

✅ **Cadena que SÍ pertenece:** `abcd`
- Recorrido esperado: a → b → c → d
- Resultado: ACEPTADA

❌ **Cadena que NO pertenece:** `abc`
- Razón: Falta la 'd' final
- Resultado: RECHAZADA

**Otras cadenas que SÍ pertenecen:** `ad`, `abd`, `acd`, `abbbcd`, `acccd`

**Otras cadenas que NO pertenecen:** `a`, `d`, `ab`, `bcd`, `adc`

---

## Expresión Regular 2: `(0|1)+`

**Descripción:** Acepta cadenas binarias no vacías (uno o más dígitos binarios).

**Operadores utilizados:**
- Unión `|`
- Cerradura positiva `+`
- Agrupación con paréntesis

### Cadenas para probar:

✅ **Cadena que SÍ pertenece:** `1010`
- Recorrido: 1 → 0 → 1 → 0
- Resultado: ACEPTADA

❌ **Cadena que NO pertenece:** (cadena vacía: presionar Enter sin escribir nada)
- Razón: Se requiere al menos un símbolo
- Resultado: RECHAZADA

**Otras cadenas que SÍ pertenecen:** `0`, `1`, `00`, `11`, `010101`, `111000`

**Otras cadenas que NO pertenecen:** `2`, `012`, `abc`, `10a`

---

## Expresión Regular 3: `x(y)?z+`

**Descripción:** Acepta 'x', opcionalmente seguida de 'y', y luego una o más 'z'.

**Operadores utilizados:**
- Concatenación (implícita)
- Opcional `?`
- Cerradura positiva `+`

### Cadenas para probar:

✅ **Cadena que SÍ pertenece:** `xyz`
- Recorrido: x → y → z
- Resultado: ACEPTADA

❌ **Cadena que NO pertenece:** `xy`
- Razón: Falta al menos una 'z' al final
- Resultado: RECHAZADA

**Otras cadenas que SÍ pertenecen:** `xz`, `xzz`, `xzzz`, `xyzzzz`

**Otras cadenas que NO pertenecen:** `x`, `y`, `z`, `yz`, `xzy`

---

## Resumen de Operadores Cubiertos

✅ Todos los operadores requeridos están presentes:

1. **Unión `|`**: Expresiones 1 y 2
2. **Concatenación (implícita)**: Todas las expresiones
3. **Cerradura de Kleene `*`**: Expresión 1
4. **Cerradura positiva `+`**: Expresiones 2 y 3
5. **Opcional `?`**: Expresión 3

---

## Guion para el Video (≤ 5 minutos)

### Introducción (30 segundos)
"Bienvenidos. En este video demostraremos nuestro programa que implementa el método directo para construir un AFD a partir de una expresión regular."

### Expresión 1 (1:20 minutos)
1. Escribir: `a(b|c)*d`
2. Mostrar tabla de transición (10 segundos)
3. Probar cadena aceptada: `abcd` (20 segundos)
4. Probar cadena rechazada: `abc` (20 segundos)

### Expresión 2 (1:20 minutos)
1. Escribir: `(0|1)+`
2. Mostrar tabla de transición (10 segundos)
3. Probar cadena aceptada: `1010` (20 segundos)
4. Probar cadena rechazada: (cadena vacía) (20 segundos)

### Expresión 3 (1:20 minutos)
1. Escribir: `x(y)?z+`
2. Mostrar tabla de transición (10 segundos)
3. Probar cadena aceptada: `xyz` (20 segundos)
4. Probar cadena rechazada: `xy` (20 segundos)

### Cierre (30 segundos)
"Como pueden observar, el programa construye correctamente el AFD usando el método directo y valida las cadenas de entrada. Gracias por su atención."

---

## Notas Técnicas

- El programa agrega automáticamente el símbolo `#` al final de la expresión regular
- Los estados se muestran como conjuntos de posiciones
- La tabla indica claramente el estado inicial (→) y los estados de aceptación (*)
- El simulador muestra el recorrido completo paso a paso

---

## Comandos para ejecutar

```bash
# Ejecutar el programa interactivo
python regex_to_dfa.py

# Para cada expresión:
# 1. Escribir la expresión regular
# 2. Observar la tabla de transición
# 3. Ingresar cadena de prueba
# 4. Presionar Enter sin texto para probar cadena vacía
# 5. Escribir 'nuevo' para cambiar de expresión
# 6. Escribir 'salir' para terminar el programa

# Ejecutar demostración automática (recomendado para video)
python demo.py
```
