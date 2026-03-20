# Guía de Ejecución - Lab 2

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

Para ejecutar la demostración automática con 2 expresiones regulares (una que no se reduce y otra que sí se reduce):

```bash
python3 demo.py
```

Este script:
- ✅ Ejecuta automáticamente 2 expresiones para cubrir la rúbrica de Lab2
- ✅ Muestra la tabla de transición del AFD original y del minimizado
- ✅ Compara estados y transiciones antes/después de minimizar
- ✅ Valida una cadena aceptada y una rechazada por cada expresión
- ⏱️ Duración aproximada: 2-3 minutos

## Para el Video de Demostración

### Opción A: Usar demo.py (Más fácil)

1. Abrir terminal
2. Ejecutar: `python3 demo.py`
3. Presionar Enter cuando se solicite para avanzar entre demostraciones
4. Grabar toda la ejecución

**Ventajas:**
- Más rápido y sin errores
- Muestra todo lo requerido automáticamente
- Fácil de editar el video

### Opción B: Usar regex_to_dfa.py (Más interactivo)

1. Abrir terminal
2. Ejecutar: `python3 regex_to_dfa.py`
3. Para cada expresión:
   - Escribir: `a|b` → Ver tabla original y minimizada → Probar `a` → Probar `ab` → Escribir `nuevo`
   - Escribir: `(a|aa)*` → Ver tabla original y minimizada → Probar `aa` → Probar `b` → Escribir `nuevo`
4. Escribir: `salir`

**Ventajas:**
- Demuestra la interactividad del programa
- Más natural y "en vivo"

## Expresiones Regulares para el Video

### 1. `a|b` (AFD ya mínimo)
- **Acepta:** `a`, `b`
- **Rechaza:** `ab`, `ba`, cadena vacía

### 2. `(a|aa)*` (AFD se reduce)
- **Acepta:** cadena vacía, `a`, `aa`, `aaa`
- **Rechaza:** `b`, `ab`, `ba`

Estas dos expresiones cumplen el requisito clave de Lab2:
- un caso donde la minimización no cambia el autómata,
- y otro donde sí reduce estados/transiciones.

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

1. **Tiempo:** El demo.py dura ~2-3 minutos (perfecto para el límite de 5 min)
2. **Claridad:** Usar terminal en pantalla completa con fuente grande
3. **Narración sugerida:**
   - Inicio: "Demostraremos el método directo para construir un AFD"
   - Por cada expresión: "Probamos la expresión... observen la tabla..."
   - Final: "Todos los operadores requeridos están cubiertos"
4. **Edición:** Pueden acelerar ligeramente las pausas si es necesario

## Solución de Problemas

### Error: "python: command not found"
- Verificar que Python esté instalado: `python3 --version`
- Usar `python3` en lugar de `python`

### El programa rechaza todas las cadenas
- Verificar que la expresión regular esté bien escrita
- Los operadores `*`, `+`, `?` son postfijos: `a*` no `*a`
- La concatenación es implícita: `ab` no `a.b`

### Caracteres especiales
- Si necesitan usar paréntesis literales en Windows, pueden necesitar comillas
- Para el laboratorio, las letras y números simples son suficientes

## Entrega

**Fecha límite:** Jueves 19 de marzo de 2026, 19:00 horas

**Verificación antes de entregar:**
✅ Video grabado y subido a YouTube (≤ 5 minutos)
✅ Código fuente incluido
✅ 2 expresiones regulares demostradas
✅ AFD original y AFD minimizado mostrados para cada expresión
✅ Comparación de estados y transiciones mostrada en ambos casos
✅ 1 cadena aceptada y 1 rechazada por expresión
✅ Un caso "ya mínimo" y otro caso "sí se reduce"
✅ Sin uso de librerías de regex

¡Éxito con el laboratorio! 🎉
