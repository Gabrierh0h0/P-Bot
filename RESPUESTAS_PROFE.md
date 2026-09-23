# Respuestas para el profe — revisión de P-Bot

Antes de responder, me metí de lleno al repo: los dos commits que hay, la rama que quedó sin fusionar, el notebook con todo lo que ya se corrió, y los documentos de la sesión. No quise asumir nada de lo que ya estaba hecho, así que todo lo que digo abajo lo puedo mostrar con el archivo o el commit exacto donde está.

## 1. ¿Qué cambió CODEX?

Hay un commit — `4d64bf3 "makers: add guided reliability improvement"`, del 25 de agosto — donde se agregaron cuatro archivos: `MAKERS_REVIEW.md` con un diagnóstico del proyecto, `TEAM_ROTATION.md` para que el equipo rote roles, y `evals/eval_cases.json` con `evals/results.md`, que son cinco casos de prueba (pedido completo, pedido incompleto, producto ambiguo, prompt injection con descuento falso, y dirección fuera de cobertura).

Lo que casi nadie se dio cuenta: ese commit está solo en la rama `origin/makers/review` y **nunca se fusionó a main**. O sea, si uno clona el repo tal como está publicado, no ve nada de esto. En `main` solo está el commit de Gabriel con el notebook, el documento de la sesión y la presentación.

## 2. ¿Qué riesgo técnico encontré?

El diagnóstico que dejó CODEX está bien encaminado — identifica que la IA podría inventar productos, precios o descuentos — pero cuando me puse a revisar el código real, la cosa está peor de lo que suena en el papel:

- No hay ni una línea que valide contra el menú. Busqué la palabra "menu" en todo el notebook y da cero resultados. En el documento de planeación el equipo escribió que "el menú siempre es la fuente de verdad, nunca un dato que la IA pueda inventar", pero eso se quedó solo en el papel, nunca se programó.
- El JSON de salida no tiene un esquema fijo: se lo inventa el modelo cada vez que corre (celda 11 del notebook). En una corrida que quedó guardada, terminó con la dirección repetida en dos campos distintos (`domicilio` y `dirección`) y sin el campo del costo de domicilio que sí estaba en el diseño original. Si algún sistema de cocina tuviera que leer ese JSON, se rompería cada vez que se vuelva a correr el notebook.
- Y el caso más delicado, el de pedir un descuento del 100% con prompt injection, no se resistió — se rompió. El modelo devolvió una respuesta vacía y el `json.loads()` explotó con una excepción que nadie manejó. Eso quedó guardado tal cual en el notebook. No es que el sistema se haya defendido, es que falló feo cuando lo atacaron.

## 3. ¿Qué eval falla o falta?

Los cinco casos de `evals/eval_cases.json` nunca se llegaron a correr — `evals/results.md` tenía las cinco filas en "Pendiente". No había código que leyera ese archivo y lo comparara contra el prototipo, estaban totalmente desconectados.

Encima hay un desajuste que pasa desapercibido: el eval espera un campo `requires_human_review` en inglés, pero lo que realmente produce el prototipo es `requiere_revision` en español, y ese nombre ni siquiera aparece en el código del notebook. Y el caso de "producto no disponible" — uno de los tres que pediste — no tenía ni un eval ni una línea de código que lo cubriera.

## 4. ¿Qué haríamos primero si esto fuera un producto real?

Lo primero sería fijar el contrato de salida de una vez por todas, escrito por el equipo, no algo que el modelo se inventa cada vez que corre. Y lo más urgente de verdad: construir la validación que hoy no existe — código normal, sin IA de por medio, que reciba lo que sacó el modelo y lo compare contra un menú real, recalcule el total aparte, y revise si la dirección está en zona de cobertura. El modelo no debería poder confirmar precios ni descuentos por su cuenta; ahora mismo puede, porque no hay nada después que lo revise. Después de eso, arreglar el manejo de errores para que una respuesta vacía o rota nunca termine en una excepción, sino en "esto lo tiene que ver una persona". Solo ahí valdría la pena ponerse a afinar prompts.

## 5. ¿Qué parte del repo no aguantaría la revisión de un ingeniero senior?

Tres cosas, de la más grave a la menos grave:

1. Que la validación contra el menú — la mitigación del riesgo principal que el equipo mismo identificó por escrito — nunca se convirtió en código. Es una promesa en un `.md`, no una función.
2. Que el trabajo de evals y revisión exista solo en una rama que nadie fusionó. Desde `main` es como si no existiera. Un PR abierto y olvidado es justo la señal de que no hay disciplina de integración.
3. Que el único caso adversarial que sí se corrió (el del descuento falso) haya terminado en una excepción sin manejar, guardada en el notebook como si fuera un resultado más de una tabla, sin que nadie la marcara como el hallazgo grave que realmente es.

---

*Aparte de esto, ya dejé listo mi propio commit (`validador_pedido.py` + tests + evals conectados) resolviendo justo los tres casos que mencionaste — ambiguos, no disponibles y descuentos falsos — como mi aporte individual en el repo.*
