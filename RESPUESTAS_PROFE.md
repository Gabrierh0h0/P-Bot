# Respuestas para el Profesor — Evaluacion Tecnica de P-Bot

Revision directa del repositorio, commits previos, ramas y ejecucion de notebooks.

---

### 1. ¿Qué cambió CODEX?
En el commit `4d64bf3` (en la rama `origin/makers/review`) se agregaron `MAKERS_REVIEW.md`, `TEAM_ROTATION.md`, `evals/eval_cases.json` y `evals/results.md`. Estos archivos estructuraron 5 casos de prueba iniciales, pero **nunca se fusionaron a `main`** ni se conectaron a código ejecutable, quedando en estado "Pendiente".

---

### 2. ¿Qué riesgo técnico encontré?
- **Falta de fuente de verdad en código**: El menú nunca se validaba programáticamente; todo dependía de la confianza ciega en el LLM.
- **Inconsistencia de esquema**: El JSON variaba de formato entre ejecuciones (campos duplicados o faltantes).
- **Vulnerabilidad a ataques**: En el caso de prompt injection con descuento falso, el sistema no manejó la respuesta y arrojó una excepción no controlada (`json.loads()`), interrumpiendo el flujo.

---

### 3. ¿Qué eval falla o falta?
- **Evals desconectados**: Los casos en `eval_cases.json` no contaban con script ejecutable ni validación automática.
- **Casos faltantes**: No existía un caso aislado para **producto no disponible** (agotado en menú).
- **Desajuste de campos**: El eval buscaba `requires_human_review` mientras que el prototipo generaba variables distintas en español.

---

### 4. ¿Qué haríamos primero si esto fuera un producto real?
1. **Definir un contrato de datos estricto**: Establecer esquemas inmutables para la comunicación entre el LLM y el backend.
2. **Capa determinista de validación**: Implementar código sin IA que contraste productos contra catálogo, recalcule subtotales/totales y verifique zonas de cobertura.
3. **Manejo resiliente de excepciones**: Asegurar que respuestas malformadas o ataques adversariales se marquen automáticamente para revisión humana (`requiere_revision: true`) sin romper el servicio.

---

### 5. ¿Qué parte del repo no aguantaría la revisión de un ingeniero senior?
1. **Reglas de negocio ausentes en código**: Prometer validación de menú en la documentación pero no tener una sola línea implementada.
2. **Falta de integración continua**: Mantener trabajo crítico de evaluación en ramas huérfanas sin merge a la rama principal.
3. **Excepciones no capturadas en producción**: Aceptar caídas en llamadas de parsing como comportamiento normal frente a entradas adversariales.

---
*Implementación técnica de respaldo disponible en `validador_pedido.py`, suite de pruebas en `tests/test_validador_pedido.py` y runner en `evals/run_evals.py`.*
