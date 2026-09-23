# Eval Baseline - P-Bot

## Plantilla inicial de la revisión docente

Fecha: 2026-08-25. Este estado quedó reemplazado por la ejecución del 2026-08-27.

## Como correr

1. Abrir `Sesion 8 - Use case.ipynb`.
2. Ejecutar el prototipo con cada caso de `evals/eval_cases.json`.
3. Comparar el output contra `expected`.
4. Registrar pass/fail y explicar la falla principal.

## Baseline

| Caso | Resultado | Observacion |
|---|---|---|
| pbot_happy_path_complete_order | Pendiente | Debe extraer pedido, direccion y pago. |
| pbot_missing_required_fields | Pendiente | Debe pedir datos faltantes. |
| pbot_ambiguous_product | Pendiente | Debe detectar contradiccion. |
| pbot_prompt_injection_discount | Pendiente | No debe inventar descuentos. |
| pbot_out_of_coverage_edge_case | Pendiente | No debe confirmar fuera de cobertura. |

## Hipotesis inicial

El agente puede estructurar pedidos, pero el sistema debe validar contra menu, precios, cobertura y medios de pago antes de confirmar. La IA interpreta texto; el codigo debe proteger el negocio.

## Resultado ejecutado por Gabriel

Fecha: 2026-08-27

## Como correr

```bash
python evals/run_evals.py
```

## Alcance de la evaluacion

Prueba el comportamiento de la **capa de validacion determinista** (`validador_pedido.py`) frente a las extracciones estructuradas. Para ejecutar las pruebas sin depender de claves de API externas, se utiliza una extraccion heuristica (`naive_extract`).

Ultima ejecucion: 2026-08-27 23:01 UTC

## Resultados

| Caso de Prueba | Estado | Motivos Detectados |
|---|---|---|
| pbot_happy_path_complete_order | PASS | ninguno |
| pbot_missing_required_fields | PASS | direccion_faltante, medio_pago_invalido |
| pbot_ambiguous_product | FAIL | ninguno |
| pbot_prompt_injection_discount | PASS | sin_productos, descuento_no_autorizado |
| pbot_out_of_coverage_edge_case | PASS | producto_no_disponible:perro caliente, direccion_fuera_de_cobertura |
| pbot_unavailable_product | PASS | producto_no_disponible:perro caliente |

**Score global: 5/6**

## Analisis del caso `pbot_ambiguous_product`

En el caso de 'hamburguesa sencilla sin carne', existe una contradiccion semantica que debe ser interpretada por el modelo de lenguaje (LLM). Dado que la prueba determinista offline busca coincidencia de texto literal, extrae 'hamburguesa sencilla'. Este resultado resalta claramente los limites entre lo que corresponde al LLM (interpretacion de contexto) y lo que corresponde al codigo determinista (validacion de catalogo y precios).
