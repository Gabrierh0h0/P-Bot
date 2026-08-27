# Revisión de P-Bot

## Lo que encontramos
- El bot toma pedidos de comida por WhatsApp y organiza los datos con IA.
- El notebook usaba el modelo de lenguaje para sacar la información, pero no había nada de código que verificara si los platos existían o si los precios eran correctos.
- Existía el riesgo de que el bot confirmara cosas que no están en el menú o que aceptara descuentos inventados por el cliente.

## Lo que se mejoró
- Se organizaron 6 casos de prueba en `evals/eval_cases.json` (pedidos completos, incompletos, confusos, descuentos falsos, fuera de cobertura y platos agotados).
- Se creó una función de validación determinista para que los precios se sumen directamente desde el menú y no desde lo que diga el chat.
