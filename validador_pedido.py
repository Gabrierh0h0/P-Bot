"""
validador_pedido.py
Modulo de validacion determinista para pedidos de P-Bot.

Proposito:
Proteger el negocio verificando las extracciones de LLM contra fuentes de verdad reales:
- Menu fijo y disponibilidad
- Precios oficiales y recálculo de totales
- Zonas de cobertura de domicilios
- Medios de pago autorizados
- Deteccion y bloqueo de descuentos no autorizados (mitigacion de prompt injection)
"""

from __future__ import annotations

import difflib
import unicodedata
from typing import Any

# Fuente de verdad: Menu oficial del restaurante con precios y disponibilidad
MENU: dict[str, dict[str, Any]] = {
    "hamburguesa sencilla": {"precio": 18000, "disponible": True},
    "hamburguesa doble": {"precio": 24000, "disponible": True},
    "papas a la francesa": {"precio": 7000, "disponible": True},
    "gaseosa": {"precio": 4000, "disponible": True},
    "limonada grande": {"precio": 8000, "disponible": True},
    "pizza personal": {"precio": 16000, "disponible": True},
    "pizza familiar": {"precio": 45000, "disponible": True},
    "perro caliente": {"precio": 14000, "disponible": False},  # Producto no disponible / agotado
}

# Prefijos validos dentro del perimetro de entrega
ZONAS_COBERTURA_PREFIJOS = ("cra", "carrera", "cll", "calle", "av", "transversal", "diagonal")

# Medios de pago soportados
MEDIOS_PAGO_VALIDOS = {"nequi", "daviplata", "efectivo", "tarjeta", "transferencia"}

COSTO_DOMICILIO_ZONA = 5000

# Descuentos vigentes autorizados por el restaurante (vacio = sin promociones activas)
# Ningun descuento dictado en el chat por el cliente se aplica sin estar aqui registrado
DESCUENTOS_VIGENTES: dict[str, float] = {}


def _normalizar(texto: str | None) -> str:
    """Normaliza texto removiendo tildes, espacios extra y pasando a minusculas."""
    if not texto:
        return ""
    texto = texto.strip().lower()
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


def _buscar_producto(nombre: str | None) -> tuple[str | None, str]:
    """
    Busca un producto en el catalogo oficial.
    Retorna: (clave_menu, estado)
    Estados posibles: 'ok', 'producto_ambiguo', 'producto_no_reconocido'
    """
    if not nombre:
        return None, "producto_ambiguo"

    clave = _normalizar(nombre)
    if clave in MENU:
        return clave, "ok"

    coincidencias = difflib.get_close_matches(clave, MENU.keys(), n=1, cutoff=0.72)
    if coincidencias:
        return coincidencias[0], "producto_ambiguo"

    return None, "producto_no_reconocido"


def _direccion_en_cobertura(direccion: str | None) -> bool:
    """Verifica si la direccion pertenece al perimetro de cobertura."""
    if not direccion:
        return False
    d = _normalizar(direccion)
    return any(prefijo in d for prefijo in ZONAS_COBERTURA_PREFIJOS)


def validar_pedido(extraccion_llm: dict[str, Any], mensaje_original: str = "") -> dict[str, Any]:
    """
    Valida la salida de un modelo de lenguaje contra reglas de negocio deterministas.
    
    Garantiza:
    1. Que los productos existan y esten disponibles.
    2. Que los precios y totales se recalculen de forma exacta.
    3. Que la direccion este dentro de la zona de cobertura.
    4. Que los medios de pago sean validos.
    5. Que cualquier intento de descuento no autorizado o prompt injection sea marcado para revision.
    """
    motivos: list[str] = []

    # Validacion de productos
    productos_crudos = extraccion_llm.get("productos") or []
    productos_validados = []
    subtotal = 0
    hubo_producto_valido = False

    for item in productos_crudos:
        if not isinstance(item, dict):
            item = {"nombre": item if isinstance(item, str) else None}

        nombre_pedido = item.get("nombre")
        cantidad_raw = item.get("cantidad") or 1
        try:
            cantidad = int(cantidad_raw)
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

        info_prod = MENU[clave_menu]
        if not info_prod["disponible"]:
            motivos.append(f"producto_no_disponible:{clave_menu}")
            productos_validados.append(
                {"nombre_pedido": clave_menu, "estado": "no_disponible", "precio_unitario": None}
            )
            continue

        precio_unitario = info_prod["precio"]
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

    # Validacion de direccion y cobertura
    direccion = (
        extraccion_llm.get("direccion_entrega")
        or extraccion_llm.get("direccion")
        or extraccion_llm.get("dirección")
        or extraccion_llm.get("domicilio")
    )
    en_cobertura = _direccion_en_cobertura(direccion)
    if not direccion:
        motivos.append("direccion_faltante")
        costo_domicilio = None
    elif not en_cobertura:
        motivos.append("direccion_fuera_de_cobertura")
        costo_domicilio = None
    else:
        costo_domicilio = COSTO_DOMICILIO_ZONA

    # Validacion de medio de pago
    medio_pago = extraccion_llm.get("medio_pago") or extraccion_llm.get("medio_de_pago")
    medio_pago_norm = _normalizar(medio_pago)
    if medio_pago_norm not in MEDIOS_PAGO_VALIDOS:
        motivos.append("medio_pago_invalido")
        medio_pago_final = None
    else:
        medio_pago_final = medio_pago_norm

    # Proteccion contra manipulacion de promociones y descuentos
    texto_eval = " ".join(
        [
            _normalizar(mensaje_original),
            _normalizar(str(extraccion_llm.get("descuento", ""))),
            _normalizar(str(extraccion_llm.get("promocion", ""))),
        ]
    )
    palabras_promo = ("descuento", "gratis", "0 pesos", "promo", "regalo", "gratuito")
    tiene_solicitud_descuento = any(p in texto_eval for p in palabras_promo)
    descuento_aplicable = 0.0

    if tiene_solicitud_descuento:
        motivos.append("descuento_no_autorizado")

    # Calculo seguro de total
    if hubo_producto_valido and costo_domicilio is not None:
        total = subtotal - int(descuento_aplicable) + costo_domicilio
    else:
        total = None

    # Deteccion de discrepancias si el LLM emitio un total arbitrario
    total_modelo = extraccion_llm.get("total")
    if total is not None and isinstance(total_modelo, (int, float)) and total_modelo != total:
        motivos.append(f"total_no_coincide:modelo={total_modelo},recalculado={total}")

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
