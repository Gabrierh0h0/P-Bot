# Makers Review — Diagnostico P-Bot

## Hallazgos Principales

- **Objetivo del bot**: Procesar pedidos de restaurante recibidos por WhatsApp extrayendo productos, cantidades, direcciones y medios de pago.
- **Estado del prototipo**: Utiliza NVIDIA NIM y Pydantic en Jupyter Notebook para estructurar el mensaje del usuario en JSON.
- **Vulnerabilidad detectada**: El sistema confiaba enteramente en la salida del LLM sin contrastarla con una fuente de verdad (menú, precios reales, zonas de entrega y promociones autorizadas).

## Mejoras Integradas

Se incorporó un marco de evaluación sistemático con `evals/eval_cases.json` que cubre:
1. **Happy path**: Pedido completo y estructurado.
2. **Campos faltantes**: Información incompleta que no debe enviarse a cocina.
3. **Ambigüedad**: Productos no especificados o frases informales ("la de siempre").
4. **Prompt injection**: Intentos de forzar descuentos del 100% o alterar precios.
5. **Fuera de cobertura**: Direcciones fuera de la zona de reparto.
6. **Producto no disponible**: Ítems del menú temporalmente agotados.

Se definió además `evals/results.md` para seguimiento de métricas y `TEAM_ROTATION.md` para coordinar el trabajo en equipo.

## Regla de Oro

> La IA interpreta la intención del usuario; el código determinista protege las reglas de negocio y los ingresos del restaurante.
