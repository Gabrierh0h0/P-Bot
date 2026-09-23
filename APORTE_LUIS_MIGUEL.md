# Aporte individual — Luis Miguel Brito Rincón

## Contexto

El profe pidió una contribución individual clara en GitHub, tomando uno de estos casos: pedidos ambiguos, productos no disponibles o descuentos falsos. Antes de escribir código revisé el repo completo (`main` y la rama `origin/makers/review`, que tiene la revisión guiada de CODEX/Emmanuel Maya y nunca se fusionó) para no duplicar trabajo ni asumir nada sobre lo que ya existía.

## Qué encontré

- Ningún archivo del repo compara lo que extrae el modelo contra una fuente de verdad real. `grep -c "menu"` sobre todo el código del notebook: **0**.
- El caso adversarial de descuento falso (Parte 7 del notebook, celda ya ejecutada) rompe el parseo de JSON con una excepción sin manejar — no hay evidencia de que el sistema lo haya rechazado correctamente, solo de que falló.
- `evals/eval_cases.json` (de la revisión de CODEX) nunca se conectó a ningún código: `evals/results.md` tenía las 5 filas en "Pendiente".
- El caso "producto no disponible" — uno de los tres que pidió el profe explícitamente — no estaba cubierto por ningún eval ni por ningún código.

## Qué agregué (cubre los tres casos pedidos)

- **`validador_pedido.py`** — capa determinista, sin LLM, sin dependencias de red. Menú fijo con precios y disponibilidad, zonas de cobertura, medios de pago válidos, y un diccionario de descuentos vigentes (vacío a propósito: ningún descuento del chat se aplica jamás). Recalcula subtotal y total desde el menú, nunca copia lo que dice el modelo o el cliente. Detecta:
  - **Producto ambiguo** — nombre parecido pero no exacto a algo del menú (`difflib`), o vacío/no reconocido.
  - **Producto no disponible** — coincide con el menú pero está marcado `disponible: False` (ej. "perro caliente").
  - **Descuento falso** — cualquier mención de descuento/gratis/promo en el mensaje o en la extracción del modelo que no esté en `DESCUENTOS_VIGENTES` se ignora y se marca para revisión.
  - Además: dirección fuera de cobertura, medio de pago inválido, y total que no cuadra con lo recalculado (señal de manipulación).
- **`tests/test_validador_pedido.py`** — 7 pruebas, corridas y pasando (`python -m pytest tests/ -v`), incluyendo los 3 casos del profe con datos realistas (uno tomado literalmente del output ya guardado en el notebook).
- **`evals/run_evals.py`** — conecta por fin `evals/eval_cases.json` con código real y regenera `evals/results.md` con resultados verdaderos (antes decía "Pendiente" en todo). Agregué también un 6º caso (`pbot_unavailable_product`) que faltaba. Resultado actual: **5/6**, con el único FAIL explicado en el propio `results.md` (no escondido): la extracción "ingenua" que uso para no depender de `NVIDIA_API_KEY` no entiende contradicciones semánticas como "hamburguesa sin carne" — eso sigue siendo trabajo del LLM, no de esta capa.
- **Celdas nuevas en `Sesión 8 - Use case.ipynb`** (Parte 11) que conectan `validador_pedido.py` directamente al `run_prototype()` que ya existía, mostrando los tres casos en vivo.

## Cómo probarlo

```
python -m pytest tests/ -v        # 7/7 debe pasar, sin API key
python evals/run_evals.py         # regenera evals/results.md, 5/6
```

Y en el notebook: correr la Parte 11 al final, después de tener `NVIDIA_API_KEY` configurada (usa el mismo `run_prototype()` de la Parte 6).

## Qué queda pendiente (para ser honesto, no para inflar el aporte)

- El extractor "ingenuo" de `evals/run_evals.py` es un reemplazo temporal de la extracción del LLM, solo para poder correr evals sin costo de API. Cuando el equipo tenga la key, deberían correr los mismos casos con `run_prototype()` real y comparar.
- La detección de contradicciones semánticas en modificadores ("sin carne" en una hamburguesa) sigue siendo responsabilidad del LLM — `validador_pedido.py` no la resuelve y no debería fingir que sí.
- El menú, la cobertura y los medios de pago siguen siendo constantes en el código; en un producto real vendrían de una base de datos administrada por el restaurante.
