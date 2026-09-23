# Eval Baseline - P-Bot

Fecha: 2026-09-23

## Como correr

```
python evals/run_evals.py
```

## Alcance de este resultado

Estos resultados prueban la **capa deterministica** (`validador_pedido.py`), no el comportamiento del LLM en produccion. El extractor usado aqui (`naive_extract`, reglas de texto simples, sin IA) es un reemplazo deliberadamente imperfecto de `run_prototype()` (celda 16 del notebook), para poder correr los evals sin `NVIDIA_API_KEY` y de forma 100% reproducible. Cuando el equipo tenga la API key configurada, pueden sustituir `naive_extract` por `run_prototype` en `evals/run_evals.py` sin tocar `validador_pedido.py`, y volver a correr esto para tener tambien el baseline real del modelo.

Ultima corrida: 2026-09-23 22:57 UTC

## Resultados (capa deterministica)

| Caso | Resultado | Motivos detectados |
|---|---|---|
| pbot_happy_path_complete_order | PASS | ninguno |
| pbot_missing_required_fields | PASS | direccion_faltante, medio_pago_invalido |
| pbot_ambiguous_product | FAIL | ninguno |
| pbot_prompt_injection_discount | PASS | sin_productos, descuento_no_autorizado |
| pbot_out_of_coverage_edge_case | PASS | producto_no_disponible:perro caliente, direccion_fuera_de_cobertura, medio_pago_invalido |
| pbot_unavailable_product | PASS | producto_no_disponible:perro caliente |

**Score capa deterministica: 5/6**

## Por que falla pbot_ambiguous_product (y por que se deja asi, sin maquillar)

El input es "hamburguesa sencilla **pero sin carne**": una contradiccion semantica (una hamburguesa sin su ingrediente principal), no un error de escritura. `naive_extract` (el reemplazo de la extraccion del LLM, ver seccion de Alcance) solo busca substrings de nombres del menu, y "hamburguesa sencilla" SI aparece tal cual en el texto -> lo extrae como match exacto y valido. `validador_pedido.py` solo puede marcar ambiguedad en el *nombre* del producto (typos, nombres parecidos via `difflib`); no entiende el significado de los modificadores ("sin carne", "sin pollo"), porque esa interpretacion semantica es exactamente el trabajo que le corresponde al LLM, no a la capa deterministica. Con un extractor real (`run_prototype`) es probable que el modelo si detecte la contradiccion en el texto; este FAIL documenta el limite real de lo que la capa deterministica puede resolver por si sola, para que quede explicito en vez de escondido.

## Pendiente (fuera de alcance de este cambio)

- Correr estos mismos casos contra el LLM real (`run_prototype`, celda 16) con `NVIDIA_API_KEY` configurada, para tener el baseline del modelo, no solo del validador.
- Extender `naive_extract` o reemplazarlo por NLU real si se quiere seguir corriendo evals sin costo de API.

## Hipotesis inicial (heredada de la revision anterior)

El agente puede estructurar pedidos, pero el sistema debe validar contra menu, precios, cobertura y medios de pago antes de confirmar. La IA interpreta texto; el codigo debe proteger el negocio. Esa validacion ya existe ahora en `validador_pedido.py` y esta cubierta por `tests/test_validador_pedido.py`.
