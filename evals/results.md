# Eval Baseline - P-Bot

Fecha: 2026-08-25

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

