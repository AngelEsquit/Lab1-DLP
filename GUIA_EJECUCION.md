# Guía de Ejecución - Lab 01

## Archivos del Proyecto

- `regex_to_dfa.py` - Programa principal (interactivo)
- `demo.py` - Script de demostración automática (para el video)
- `README.md` - Documentación completa
- `CASOS_DE_PRUEBA.md` - Casos de prueba detallados
- `Instrucciones.md` - Instrucciones originales del laboratorio

## Opción 1: Programa Interactivo

Para usar el programa de forma interactiva:

```bash
python regex_to_dfa.py
```

### Flujo de uso:
1. Ingresar una expresión regular
2. Ver la tabla de transición generada
3. Ingresar cadenas para validar (una por una)
4. Presionar Enter sin texto para probar cadena vacía
5. Escribir "nuevo" para probar otra expresión
6. Escribir "salir" para terminar

### Ejemplo de sesión:
```
Ingrese una expresión regular: a(b|c)*d
... tabla de transición ...
Ingrese una cadena para validar: abcd
✓ CADENA ACEPTADA
Ingrese una cadena para validar: abc
✗ CADENA RECHAZADA
Ingrese una cadena para validar: nuevo
Ingrese una expresión regular: salir
```

## Opción 2: Demo Automática (Recomendado para el Video)

Para ejecutar la demostración automática con las 3 expresiones regulares y sus casos de prueba:

```bash
python demo.py
```

Este script:
- ✅ Ejecuta automáticamente las 3 expresiones regulares requeridas
- ✅ Muestra la tabla de transición de cada una
- ✅ Valida 4 cadenas por expresión (2 que aceptan, 2 que rechazan)
- ✅ Muestra el recorrido completo del AFD para cada cadena
- ✅ Verifica que todos los operadores estén cubiertos
- ⏱️ Duración aproximada: 3-4 minutos (perfecto para el video)

## Para el Video de Demostración

### Opción A: Usar demo.py (Más fácil)

1. Abrir terminal
2. Ejecutar: `python demo.py`
3. Presionar Enter cuando se solicite para avanzar entre demostraciones
4. Grabar toda la ejecución

**Ventajas:**
- Más rápido y sin errores
- Muestra todo lo requerido automáticamente
- Fácil de editar el video

### Opción B: Usar regex_to_dfa.py (Más interactivo)

1. Abrir terminal
2. Ejecutar: `python regex_to_dfa.py`
3. Para cada expresión:
   - Escribir: `a(b|c)*d` → Ver tabla → Probar `abcd` → Probar `abc` → Escribir `nuevo`
   - Escribir: `(0|1)+` → Ver tabla → Probar `1010` → Probar cadena vacía (solo Enter) → Escribir `nuevo`
   - Escribir: `x(y)?z+` → Ver tabla → Probar `xyz` → Probar `xy` → Escribir `nuevo`
4. Escribir: `salir`

**Ventajas:**
- Demuestra la interactividad del programa
- Más natural y "en vivo"

## Expresiones Regulares para el Video

Las tres expresiones preparadas son:

### 1. `a(b|c)*d`
- **Acepta:** `abcd`, `ad`, `abbbcd`
- **Rechaza:** `abc`, `a`, `d`

### 2. `(0|1)+`
- **Acepta:** `1010`, `0`, `111000`
- **Rechaza:** (cadena vacía), `2`, `abc`

### 3. `x(y)?z+`
- **Acepta:** `xyz`, `xz`, `xyzzzz`
- **Rechaza:** `xy`, `x`, `yz`

## Verificación de Operadores

✅ Todos los operadores requeridos están presentes:

| Operador | Expresión |
|----------|-----------|
| Unión `\|` | Expresiones 1 y 2 |
| Concatenación | Todas |
| Kleene `*` | Expresión 1 |
| Positivo `+` | Expresiones 2 y 3 |
| Opcional `?` | Expresión 3 |

## Estructura de la Salida

El programa muestra:

1. **Construcción del AFD:**
   - Número de estados
   - Alfabeto extraído

2. **Tabla de Transición:**
   - Estados (S0, S1, S2, ...)
   - Transiciones para cada símbolo
   - Marcadores: `->` inicio, `*` aceptación
   - Detalle de posiciones en cada estado

3. **Validación de Cadenas:**
   - Recorrido paso a paso
   - Estado actual → símbolo → siguiente estado
   - Resultado: ACEPTADA o RECHAZADA
   - Razón del rechazo si aplica

## Consejos para el Video

1. **Tiempo:** El demo.py dura ~3-4 minutos (perfecto para el límite de 5 min)
2. **Claridad:** Usar terminal en pantalla completa con fuente grande
3. **Narración sugerida:**
   - Inicio: "Demostraremos el método directo para construir un AFD"
   - Por cada expresión: "Probamos la expresión... observen la tabla..."
   - Final: "Todos los operadores requeridos están cubiertos"
4. **Edición:** Pueden acelerar ligeramente las pausas si es necesario

## Solución de Problemas

### Error: "python: command not found"
- Verificar que Python esté instalado: `python --version`
- En algunos sistemas usar: `python3` en lugar de `python`

### El programa rechaza todas las cadenas
- Verificar que la expresión regular esté bien escrita
- Los operadores `*`, `+`, `?` son postfijos: `a*` no `*a`
- La concatenación es implícita: `ab` no `a.b`

### Caracteres especiales
- Si necesitan usar paréntesis literales en Windows, pueden necesitar comillas
- Para el laboratorio, las letras y números simples son suficientes

## Entrega

**Fecha límite:** Jueves 12 de marzo de 2025, 19:00 horas

**Verificación antes de entregar:**
✅ Video grabado y subido a YouTube (≤ 5 minutos)
✅ Código fuente incluido
✅ 3 expresiones regulares demostradas
✅ Tabla de transición mostrada para cada una
✅ 1 cadena aceptada y 1 rechazada por expresión
✅ Todos los operadores presentes (|, concatenación, *, +, ?)
✅ Sin uso de librerías de regex

¡Éxito con el laboratorio! 🎉
