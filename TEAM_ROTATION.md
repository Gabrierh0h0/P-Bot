# Team Rotation

Objetivo: que todos entiendan todo el sistema, no que cada persona quede encerrada en una parte.

## Semana actual

| Rol temporal | Responsable | Que lidera | Quien debe poder explicarlo |
|---|---|---|---|
| Build owner | Gabriel Alejandro | Integracion del notebook con el flujo principal | Luis Miguel |
| Evaluate owner | Luis Miguel | Validador determinista, tests y eval runner | Gabriel Alejandro |
| Explain owner | Ambos | Arquitectura, resultados y demo tecnica | Ambos |

## Reglas

- El owner lidera, pero no trabaja aislado.
- Cada cambio debe poder ser explicado por otra persona del equipo.
- Cada integrante debe hacer al menos un microcambio visible en GitHub.
- No cuenta decir "yo ayude" si no hay evidencia en el repo.
- No se cambia todo a la vez: una hipotesis, un cambio, una medicion.

## Checklist semanal

- [ ] Todos entienden el flujo principal.
- [ ] Todos entienden los evals.
- [ ] Todos pueden explicar el ultimo cambio.
- [ ] Todos saben que sigue fallando.
- [ ] Cada integrante dejo evidencia en GitHub.

## Preguntas que cualquiera debe responder

1. Que cambio esta semana?
2. Por que ese cambio importa?
3. Como sabemos si mejoro?
4. Que caso sigue fallando?
5. Que haremos despues?

## Acuerdo de trabajo del equipo

Para trabajar en orden nos repartimos las tareas en tres roles que vamos rotando:

- **Build (Construir):** escribir el código del validador y las funciones en Python.
- **Evaluate (Evaluar):** armar los casos de prueba y correr los evals para ver qué pasa y qué falla.
- **Explain (Explicar):** documentar lo que hicimos, responder las preguntas y explicar las decisiones tomadas.

Esta asignacion describe la integracion hecha en `makers/review`; cada integrante debe poder
explicar y modificar tambien la parte liderada por su companero.
