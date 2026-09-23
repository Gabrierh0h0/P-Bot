# Gates Makers — revisión 2026-09-23

Referencia revisada: integración local de `origin/dev/GabrielAlejandro` y `origin/luis-miguel/validador-pedidos`.

| Gate | Estado | Evidencia | Para cerrar |
|---|---|---|---|
| Arquitectura atribuible | NO PASA | No existe `docs/arquitectura.md`. | Gabriel y Luis deben documentar extractor, fuentes de verdad, validador y salida humana. |
| Uso de IA + evals | PARCIAL | Ejecución actual: 7/7 unit tests y 5/6 evals; el caso ambiguo falla y no se probó LLM real. | Ejecutar los seis casos end-to-end. |
| Jailbreak y safety | PARCIAL | Descuento falso se neutraliza en código. | Probar que el extractor comprometido tampoco confirma ni envía. |
| Mantenibilidad | PASS | Validador y tests acotados tras integrar una sola implementación. | Evitar duplicar nuevamente archivos entre ramas. |
| Producto ejecutable | NO PASA | Notebook y scripts; no hay webhook/API/app. | Endpoint mínimo que reciba mensaje y devuelva borrador/revisión. |
| Git profesional | PARCIAL | Ambos tienen ramas, pero desarrollaron archivos paralelos incompatibles; se agregó CI en `makers/review`. | Dividir ownership, PRs pequeños e integrar temprano. |

La integración de `makers/review` usa la suite de Luis Miguel y conserva la evidencia/notebook de Gabriel. Las ramas estudiantiles no fueron alteradas.
