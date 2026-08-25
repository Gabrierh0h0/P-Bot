# Makers Review

## Que encontramos

- El proyecto PeterBot/P-Bot procesa pedidos de restaurante recibidos por WhatsApp.
- El caso de uso esta bien enfocado: texto desordenado, datos faltantes, menu, precios y cobertura.
- El notebook usa NVIDIA NIM y Pydantic para estructurar el flujo.
- No habia README principal ni evals versionados en el repo.
- El riesgo principal es confirmar pedidos con productos, precios, direccion o descuentos inventados.

## Mejora aplicada

Agregue `evals/eval_cases.json` con 5 casos:

- pedido completo;
- pedido incompleto;
- producto ambiguo;
- prompt injection con descuento falso;
- direccion fuera de cobertura.

Tambien agregue `evals/results.md` para registrar baseline y `TEAM_ROTATION.md` para que ambos integrantes roten Build, Evaluate y Explain.

## Por que importa

En un bot de pedidos, el JSON valido no basta. El sistema debe verificar contra fuentes de verdad: menu, precios, cobertura y medios de pago. La IA puede interpretar el mensaje, pero no debe tener autoridad para inventar descuentos ni confirmar pedidos imposibles.

## Como probarlo

1. Ejecutar el notebook `Sesion 8 - Use case.ipynb`.
2. Probar cada caso de `evals/eval_cases.json`.
3. Registrar pass/fail en `evals/results.md`.
4. Elegir una sola falla y formular la siguiente hipotesis de mejora.

## Tu reto

1. Core: completar baseline real para los 5 casos y reportar score `X/5`.
2. Intermediate: crear una funcion deterministica que valide productos y precios contra un menu fijo.
3. Advanced: agregar `requires_human_review` cuando haya descuento, producto ambiguo, direccion incompleta o zona fuera de cobertura.
