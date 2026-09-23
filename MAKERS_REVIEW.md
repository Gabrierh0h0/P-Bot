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

<!-- MAKERS_REVIEW_2026_08_27_START -->
## Revision docente - 2026-08-27

### Lo que vimos

- Gabriel y Luis Miguel hicieron avances fuertes y muy parecidos: validador de pedidos, tests, eval runner y documentacion individual.
- El criterio es correcto: el bot no debe inventar productos, descuentos, precios ni zonas de cobertura.
- Buen punto de Luis Miguel: el extractor temporal no reemplaza al LLM real.
- El riesgo ahora es duplicacion: dos ramas tocando casi los mismos archivos.
- El equipo necesita integrar una sola version limpia con lo mejor de ambas.

### Reto de hoy

Unifiquen las dos ramas sin perder evidencia:

1. Decidir que version de alidador_pedido.py queda como base.
2. Mantener tests y evals en una sola carpeta.
3. Dejar vals/results.md con score actual, unica falla y siguiente hipotesis.

### Tarea obligatoria: diagrama de arquitectura

Crear docs/arquitectura.md con un diagrama Mermaid que muestre:

`mermaid
flowchart LR
  ClienteWhatsApp --> MensajePedido
  MensajePedido --> ExtractorLLM
  ExtractorLLM --> PedidoEstructurado
  PedidoEstructurado --> ValidadorPedido
  MenuPrecios --> ValidadorPedido
  Cobertura --> ValidadorPedido
  ValidadorPedido --> PedidoConfirmable
  ValidadorPedido --> RevisionHumana
`

Debe quedar claro que el modelo interpreta texto, pero el negocio se protege con menu, precios, cobertura y confirmacion.

### Criterio de aceptacion

No queremos dos soluciones paralelas. Queremos una rama integrada, corrible y explicable por ambos.
<!-- MAKERS_REVIEW_2026_08_27_END -->


<!-- MAKERS_CODE_ARCH_REVIEW_2026_09_01_START -->
## Revision de codigo y arquitectura - 2026-09-01

### Lectura docente

- Gabriel y Luis Miguel hicieron avances fuertes con validadores, tests y evals.
- No se detecto docs/arquitectura.md.
- El problema ahora no es falta de ideas, sino integracion: hay soluciones paralelas tocando lo mismo.
- El riesgo principal es confirmar pedidos con productos, precios, descuentos o cobertura inventados.

### Revision de principios

- Bien: proteger negocio con menu/precios/cobertura deterministica.
- Falta: una sola version integrada y mantenible.
- Falta: arquitectura que muestre extractor LLM, validador, fuente de verdad y confirmacion.

### Pendiente de equipo

Crear docs/arquitectura.md e integrar una sola version de alidador_pedido.py, tests y evals.

### Pendiente por poca evidencia individual

Ambos tienen evidencia. El pendiente no es individual; es coordinacion de equipo y limpieza de integracion.
<!-- MAKERS_CODE_ARCH_REVIEW_2026_09_01_END -->

## Avance reportado por Gabriel

## Lo que encontramos
- El bot toma pedidos de comida por WhatsApp y organiza los datos con IA.
- El notebook usaba el modelo de lenguaje para sacar la información, pero no había nada de código que verificara si los platos existían o si los precios eran correctos.
- Existía el riesgo de que el bot confirmara cosas que no están en el menú o que aceptara descuentos inventados por el cliente.

## Lo que se mejoró
- Se organizaron 6 casos de prueba en `evals/eval_cases.json` (pedidos completos, incompletos, confusos, descuentos falsos, fuera de cobertura y platos agotados).
- Se creó una función de validación determinista para que los precios se sumen directamente desde el menú y no desde lo que diga el chat.

## Integracion docente — 2026-09-23

- Se integraron `dev/GabrielAlejandro` y `luis-miguel/validador-pedidos` solo en `makers/review`.
- Ambas ramas implementaban los mismos archivos de validador, pruebas y evals.
- Se tomo como base unica la suite de Luis Miguel por documentar mejor la frontera entre
  extraccion semantica y reglas deterministas.
- Se conservaron el notebook, el documento de aporte y la evidencia de Gabriel.
- Esta decision no declara una solucion individual como "ganadora": elimina duplicacion para
  que el equipo pueda revisar una sola base y explicar las dos contribuciones.

### Gate pendiente

El resultado 5/6 solo prueba la capa determinista con un extractor heuristico. Falta ejecutar
los mismos seis casos contra el LLM real y demostrar que `pbot_ambiguous_product` se escala a
revision humana sin depender de que el prompt sea obedecido.
