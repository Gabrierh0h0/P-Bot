# Respuestas para el profe - P-Bot

Revisé el repositorio, las ramas que habían y lo que se corrió en el notebook para responder las preguntas:

## 1. ¿Qué cambió CODEX?
En la rama `makers/review` se agregaron 4 archivos (`MAKERS_REVIEW.md`, `TEAM_ROTATION.md`, y la carpeta `evals` con los casos de prueba). El problema es que todo se quedó en esa rama y nunca se hizo merge a `main`, así que en la rama principal no se veía nada de eso. Además, los casos de prueba estaban todos en "Pendiente" porque no había un código que los corriera.

## 2. ¿Qué riesgo técnico encontré?
- El bot no revisaba los pedidos contra un menú real en el código, solo se confiaba en lo que sacara el modelo de IA.
- El formato del JSON cambiaba bastante en cada intento (a veces repetía datos o quitaba campos necesarios).
- Si alguien le metía un mensaje con trampa (como pedir 100% de descuento), el programa se caía con un error de `json.loads()` en vez de responder de forma controlada.

## 3. ¿Qué eval falla o falta?
- Hacía falta un script que de verdad corriera los casos de prueba de forma automática.
- No había ningún caso para probar cuando un producto está agotado o no disponible en el menú.
- El archivo de pruebas pedía un campo en inglés (`requires_human_review`), pero el prototipo generaba variables en español.

## 4. ¿Qué haríamos primero si esto fuera un producto real?
1. Dejar una estructura de datos fija y clara que no cambie entre llamadas.
2. Poner código normal en Python (sin IA) que revise que los productos existan en el menú, sume los precios reales y verifique que la dirección esté en la zona de entrega.
3. Si el modelo se equivoca o el cliente pide cosas raras, marcar el pedido para revisión humana (`requiere_revision = True`) en vez de dejar que el programa se caiga.

## 5. ¿Qué parte del repo no aguantaría la revisión de un ingeniero senior?
1. Que en el documento decíamos que el menú era la fuente de verdad, pero nunca se programó un menú en el código.
2. Dejar ramas olvidadas con trabajo sin fusionar a `main`.
3. Dejar que un ataque de prompt injection rompa el programa con una excepción en vez de manejar el error.
