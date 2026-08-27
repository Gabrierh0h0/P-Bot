# Mi aporte al proyecto - Gabriel Alejandro

## ¿Qué hice?
Me enfoqué en hacer que el bot sea confiable y no confirme pedidos con datos inventados o precios incorrectos. Creé una capa de validación en Python para revisar lo que extrae el modelo antes de que pase a cocina o facturación.

Me centré en tres problemas clave:
1. **Productos ambiguos o nombres raros:** si alguien pide cosas confusas como "la de siempre", el bot no inventa un producto sino que pide que alguien lo revise.
2. **Productos no disponibles:** si piden algo que no hay (como el perro caliente agotado), no lo deja pasar como pedido válido.
3. **Descuentos falsos / Prompt Injection:** si alguien intenta engañar al bot pidiendo 100% de descuento o cosas gratis, el sistema ignora ese mensaje y calcula el valor real usando los precios del menú.

## Archivos que trabajé

- `validador_pedido.py`: tiene el menú con precios fijos, lista de zonas de entrega y la función `validar_pedido()`.
- `tests/test_validador_pedido.py`: 7 pruebas unitarias para revisar que todo funcione bien (corren rápido y sin depender de internet ni de APIs).
- `evals/eval_cases.json` y `evals/run_evals.py`: agregué el caso de producto no disponible y creé el script para correr las pruebas y guardar el resumen en `evals/results.md`.
- `Sesión 8 - Use case.ipynb`: agregué la Parte 11 al final para mostrar el validador funcionando en el notebook.

## Cómo probarlo

Pruebas unitarias:
```bash
python -m unittest tests/test_validador_pedido.py
```

Evaluaciones automáticas:
```bash
python evals/run_evals.py
```
