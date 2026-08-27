# Eval Baseline - P-Bot

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
