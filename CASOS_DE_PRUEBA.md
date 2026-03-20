# Casos de Prueba para el Video de Demostración (Lab 2)

## Objetivo del Video

Mostrar dos expresiones regulares:
1. Una cuyo AFD **ya es mínimo** (no cambia al minimizar).
2. Otra cuyo AFD **sí se reduce** al minimizar.

Para cada expresión se debe mostrar:
- Tabla de transición del AFD original (método directo)
- Tabla de transición del AFD minimizado
- Comparación de estados y transiciones
- Una cadena aceptada y una rechazada, simuladas sobre el AFD minimizado

---

## Expresión 1 (AFD ya mínimo): `a|b`

**Descripción:** Acepta exactamente un símbolo: `a` o `b`.

### Cadenas para probar
- **Sí pertenece:** `a`
- **No pertenece:** `ab`

### Resultado esperado de minimización
- El número de estados y transiciones se mantiene igual.
- Debe aparecer mensaje de que el AFD ya era mínimo.

---

## Expresión 2 (AFD se reduce): `(a|aa)*`

**Descripción:** Acepta repeticiones de bloques `a` o `aa`, equivalente a `a*`.

### Cadenas para probar
- **Sí pertenece:** `aa`
- **No pertenece:** `b`

### Resultado esperado de minimización
- El AFD original debe reducirse (en este proyecto: de 2 estados a 1 estado).
- Debe aparecer mensaje de que el AFD se minimizó exitosamente.

---

## Guion sugerido (≤ 5 minutos)

### Introducción (20–30 s)
"En este video mostraremos la construcción de un AFD por método directo y su minimización."

### Caso 1: `a|b` (1:30 min)
1. Ingresar expresión
2. Mostrar tabla original
3. Mostrar tabla minimizada
4. Comparar estados/transiciones (sin cambio)
5. Probar `a` (aceptada) y `ab` (rechazada)

### Caso 2: `(a|aa)*` (1:30 min)
1. Ingresar expresión
2. Mostrar tabla original
3. Mostrar tabla minimizada
4. Comparar estados/transiciones (sí reduce)
5. Probar `aa` (aceptada) y `b` (rechazada)

### Cierre (20–30 s)
"Se demuestra un caso que ya era mínimo y otro que se reduce al minimizar."

---

## Comandos de ejecución

```bash
# Programa interactivo
python3 regex_to_dfa.py

# Demo automática para grabar
python3 demo.py
```
