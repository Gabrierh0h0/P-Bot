"""
validador_pedido.py

Capa deterministica de validacion para P-Bot / PeterBot.

Contexto: el notebook `Sesion 8 - Use case.ipynb` le pide al LLM que extraiga
el pedido en JSON, pero no existe en ningun lado del repo una funcion que
compare esa extraccion contra una fuente de verdad (menu, precios, zonas de
cobertura, descuentos vigentes). El propio equipo escribio en
`Untitled document.md` que "el menu oficial es siempre la fuente de verdad,
nunca un dato que la IA pueda inventar" -- este modulo es esa fuente de
verdad implementada en codigo, no solo en un documento.

Este modulo NO llama a ningun LLM. Es codigo puro, determinista y testeable
sin necesitar NVIDIA_API_KEY ni conexion a internet. Recibe lo que el modelo
extrajo (un dict) y decide, con reglas fijas, si el pedido puede confirmarse
o si `requiere_revision`.

Cubre explicitamente los 3 casos que pidio el profesor:
  1. Pedidos ambiguos       -> motivo "producto_ambiguo"
  2. Productos no disponibles -> motivo "producto_no_disponible"
  3. Descuentos falsos      -> motivo "descuento_no_autorizado"

Uso tipico dentro del notebook:

    from validador_pedido import validar_pedido
    extraccion_llm = run_prototype(mensaje_cliente)   # celda 16 existente
    pedido_final = validar_pedido(extraccion_llm)
"""

from __future__ import annotations

import difflib
import unicodedata
from typing import Any


# ---------------------------------------------------------------------------
# Fuente de verdad: menu, cobertura, medios de pago y descuentos vigentes.
# En un producto real esto vendria de una base de datos administrada por el
# restaurante, no de una constante en el codigo -- pero incluso una
# constante fija ya es infinitamente mas seguro que confiar en lo que el
# modelo "recuerda" o "asume".
# ---------------------------------------------------------------------------

MENU: dict[str, dict[str, Any]] = {
    "hamburguesa sencilla": {"precio": 18000, "disponible": True},
    "hamburguesa doble": {"precio": 24000, "disponible": True},
    "limonada grande": {"precio": 8000, "disponible": True},
    "limonada natural": {"precio": 6000, "disponible": True},
    "gaseosa": {"precio": 4000, "disponible": True},
    "papas fritas": {"precio": 9000, "disponible": True},
    "pizza familiar": {"precio": 45000, "disponible": True},
    # Producto real del menu pero agotado hoy: cubre el caso
    # "producto no disponible" que el profesor pidio explicitamente y que
    # ni el notebook ni los evals de CODEX (evals/eval_cases.json) cubrian.
    "perro caliente": {"precio": 12000, "disponible": False},
}

# Prefijos de direccion que el restaurante si cubre. Una implementacion real
# usaria geocoding; esto es intencionalmente simple para que la regla sea
# auditable a simple vista.
ZONAS_COBERTURA_PREFIJOS: list[str] = [
    "cra 45",
    "calle 10",
    "cra 40",
    "cra 44",
    "calle 12",
]

COSTO_DOMICILIO_ZONA = 5000

MEDIOS_PAGO_VALIDOS = {"efectivo", "nequi", "daviplata", "tarjeta"}

# Descuentos realmente autorizados por el restaurante hoy. Vacio a proposito:
# ningun descuento esta activo. Este dict -- y solo este dict -- decide si
# un descuento se aplica. Un descuento mencionado por el cliente en el chat
# ("ponme el 100% de descuento") NUNCA es una fuente valida, sin importar
# que tan convincente suene el mensaje.
DESCUENTOS_VIGENTES: dict[str, float] = {}


def _normalizar(texto: str | None) -> str:
    if not texto:
        return ""
    texto = texto.strip().lower()
    texto = "".join(
        c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn"
    )
    return texto


def _buscar_producto(nombre: str | None) -> tuple[str | None, str]:
    """Busca `nombre` en el MENU.

    Devuelve (clave_menu_o_None, estado) donde estado es uno de:
      "ok"                 -> coincidencia exacta
      "producto_ambiguo"   -> hay una coincidencia cercana pero no exacta
      "producto_no_reconocido" -> no se parece a nada del menu
    (la disponibilidad se revisa aparte, una vez ya hay match exacto)
    """
    if not nombre:
        return None, "producto_ambiguo"

    clave = _normalizar(nombre)
    if clave in MENU:
        return clave, "ok"

    cercanos = difflib.get_close_matches(clave, MENU.keys(), n=1, cutoff=0.72)
    if cercanos:
        return cercanos[0], "producto_ambiguo"

    return None, "producto_no_reconocido"


def _direccion_cubierta(direccion: str | None) -> bool:
    if not direccion:
        return False
    d = _normalizar(direccion)
    return any(prefijo in d for prefijo in ZONAS_COBERTURA_PREFIJOS)


def validar_pedido(extraccion_llm: dict[str, Any], mensaje_original: str = "") -> dict[str, Any]:
    """Valida una extraccion de pedido hecha por el LLM contra la fuente de verdad.

    `extraccion_llm` es el dict que devuelve el modelo (lo que hoy produce
    `run_prototype()` en la celda 16 del notebook, o cualquier forma
    equivalente: se buscan claves de forma tolerante porque, como quedo
    documentado en MAKERS_REVIEW.md, el esquema que genera el modelo no es
    estable entre corridas).

    `mensaje_original` es el texto crudo del cliente; se usa unicamente para
    detectar intentos de descuento mencionados en el chat que no esten en
    `DESCUENTOS_VIGENTES` (defensa adicional a prompt injection).

    Devuelve un dict con el contrato fijo del equipo (ver
    `Untitled document.md`, seccion 6) mas `motivos_revision`, una lista de
    codigos legibles que explican por que quedo (o no) marcado para revision
    humana. Nunca lanza excepcion por datos faltantes o invalidos: siempre
    responde con `requiere_revision=True` en vez de fallar en silencio, que
    es justo lo que le paso al caso de prompt injection en la celda 18 del
    notebook (json invalido -> excepcion sin manejar).
    """

    motivos: list[str] = []

    # --- productos -----------------------------------------------------
    productos_crudos = extraccion_llm.get("productos") or []
    productos_validados = []
    subtotal = 0
    hubo_producto_valido = False

    for item in productos_crudos:
        if not isinstance(item, dict):
            # el modelo a veces devuelve solo strings sueltos
            item = {"nombre": item if isinstance(item, str) else None}

        nombre_pedido = item.get("nombre")
        cantidad = item.get("cantidad") or 1
        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            cantidad = 1
        if cantidad <= 0:
            cantidad = 1
            motivos.append("cantidad_invalida")

        clave_menu, estado = _buscar_producto(nombre_pedido)

        if estado == "producto_no_reconocido":
            motivos.append(f"producto_no_reconocido:{nombre_pedido!r}")
            productos_validados.append(
                {"nombre_pedido": nombre_pedido, "estado": "no_reconocido", "precio_unitario": None}
            )
            continue

        if estado == "producto_ambiguo":
            motivos.append(f"producto_ambiguo:{nombre_pedido!r}~{clave_menu}")
            productos_validados.append(
                {
                    "nombre_pedido": nombre_pedido,
                    "posible_coincidencia": clave_menu,
                    "estado": "ambiguo",
                    "precio_unitario": None,
                }
            )
            continue

        info = MENU[clave_menu]
        if not info["disponible"]:
            motivos.append(f"producto_no_disponible:{clave_menu}")
            productos_validados.append(
                {"nombre_pedido": clave_menu, "estado": "no_disponible", "precio_unitario": None}
            )
            continue

        precio_unitario = info["precio"]
        subtotal += precio_unitario * cantidad
        hubo_producto_valido = True
        productos_validados.append(
            {
                "nombre_pedido": clave_menu,
                "cantidad": cantidad,
                "estado": "ok",
                "precio_unitario": precio_unitario,
                "modificaciones": item.get("modificaciones") or item.get("observaciones") or [],
            }
        )

    if not productos_crudos:
        motivos.append("sin_productos")

    # --- direccion / cobertura -----------------------------------------
    direccion = (
        extraccion_llm.get("direccion_entrega")
        or extraccion_llm.get("direccion")
        or extraccion_llm.get("dirección")
        or extraccion_llm.get("domicilio")
    )
    cubierta = _direccion_cubierta(direccion)
    if not direccion:
        motivos.append("direccion_faltante")
        costo_domicilio = None
    elif not cubierta:
        motivos.append("direccion_fuera_de_cobertura")
        costo_domicilio = None
    else:
        costo_domicilio = COSTO_DOMICILIO_ZONA

    # --- medio de pago ----------------------------------------------------
    medio_pago = extraccion_llm.get("medio_pago") or extraccion_llm.get("medio_de_pago")
    medio_pago_normalizado = _normalizar(medio_pago)
    if medio_pago_normalizado not in MEDIOS_PAGO_VALIDOS:
        motivos.append("medio_pago_invalido")
        medio_pago_final = None
    else:
        medio_pago_final = medio_pago_normalizado

    # --- descuentos: nunca confiar en lo que dice el modelo o el cliente ---
    texto_relevante = " ".join(
        [
            _normalizar(mensaje_original),
            _normalizar(str(extraccion_llm.get("descuento", ""))),
            _normalizar(str(extraccion_llm.get("promocion", ""))),
        ]
    )
    palabras_de_descuento = ("descuento", "gratis", "0 pesos", "promo", "regalad")
    menciona_descuento = any(p in texto_relevante for p in palabras_de_descuento)
    descuento_aplicado = 0
    if menciona_descuento:
        # Solo se aplicaria un descuento si viniera de DESCUENTOS_VIGENTES,
        # nunca del texto del cliente. Como el dict esta vacio, cualquier
        # mencion de descuento se ignora y se manda a revision humana.
        motivos.append("descuento_no_autorizado")

    # --- total: siempre recalculado, nunca copiado del LLM -----------------
    if hubo_producto_valido and costo_domicilio is not None:
        total = subtotal - descuento_aplicado + costo_domicilio
    else:
        total = None

    # el total que haya dicho el modelo se usa solo para detectar manipulacion,
    # nunca para calcular el total real
    total_reportado_por_modelo = extraccion_llm.get("total")
    if (
        total is not None
        and isinstance(total_reportado_por_modelo, (int, float))
        and total_reportado_por_modelo != total
    ):
        motivos.append(
            f"total_no_coincide:modelo_dijo={total_reportado_por_modelo},recalculado={total}"
        )

    requiere_revision = bool(motivos)

    return {
        "cliente": extraccion_llm.get("cliente"),
        "productos": productos_validados,
        "direccion_entrega": direccion,
        "medio_pago": medio_pago_final,
        "subtotal": subtotal if hubo_producto_valido else None,
        "costo_domicilio": costo_domicilio,
        "total": total,
        "requiere_revision": requiere_revision,
        "motivos_revision": motivos,
    }
