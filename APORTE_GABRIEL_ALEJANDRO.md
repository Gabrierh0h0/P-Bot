# Aporte Individual — Gabriel Alejandro

## Contexto y Objetivo
El objetivo de este aporte es robustecer el bot de pedidos **P-Bot** mediante la implementacion de una capa determinista de negocio que garantice la integridad de los pedidos y resuelva tres desafios criticos:
1. **Pedidos y productos ambiguos**: Deteccion de terminos informales o faltantes sin inventar productos.
2. **Productos no disponibles**: Bloqueo de confirmaciones para articulos agotados en el catalogo.
3. **Descuentos no autorizados / Prompt Injection**: Rechazo de intentos de alterar precios o forzar totales en 0.

---

## Modulos y Componentes Creados

1. **`validador_pedido.py`**
   - Catalogo oficial de productos con precios y banderas de disponibilidad.
   - Normalizacion de texto (remocion de diacriticos, minusculas).
   - Deteccion de proximidad (`difflib`) para identificar typos o ambiguedades.
   - Verificacion de perimetro de cobertura y medios de pago soportados.
   - Recalculo determinista de totales: el modelo nunca define el precio final.
   - Marcado automatico de pedidos sospechosos con `requiere_revision=True` y lista detallada de `motivos_revision`.

2. **`tests/test_validador_pedido.py`**
   - Suite de 7 pruebas unitarias independientes de llamadas de red o claves de API.
   - Compatible con `pytest` y `python -m unittest`.
   - Cobertura de caminos felices, ataques adversariales, direcciones fuera de cobertura, productos agotados y entradas malformadas.

3. **`evals/` (Suite de Evaluacion)**
   - `evals/eval_cases.json`: Dataset estructurado con 6 casos de prueba (incluyendo el caso de producto no disponible).
   - `evals/run_evals.py`: Script automatizado para ejecutar las evaluaciones y actualizar metricas.
   - `evals/results.md`: Reporte detallado del baseline determinista (5/6 pass con explicacion tecnica del caso semantico).

4. **Integracion en Notebook (`Sesión 8 - Use case.ipynb`)**
   - Agregada la **Parte 11: Validacion determinista**, demostrando en vivo como el validador procesa las salidas del prototipo y previene errores en tiempo de ejecucion.

---

## Como Ejecutar y Validar

### 1. Pruebas Unitarias
```bash
python -m unittest tests/test_validador_pedido.py
```
*(7/7 pruebas deben pasar exitosamente)*

### 2. Evaluacion de Evals
```bash
python evals/run_evals.py
```
*(Actualiza la matriz de resultados en `evals/results.md`)*

---

## Conclusiones Tecnicas
- Separar la extraccion semantica (a cargo del LLM) de la validacion transaccional (a cargo de codigo determinista) elimina los riesgos de alucinacion de precios y ataques de inyeccion en entornos de comercio conversacional.
