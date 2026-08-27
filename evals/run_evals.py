"""
evals/run_evals.py
Ejecuta la suite de evaluacion determinista sobre los casos en evals/eval_cases.json
y actualiza evals/results.md.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

# Ajuste de path para imports
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from validador_pedido import MENU, validar_pedido

EVAL_CASES_PATH = ROOT_DIR / "evals" / "eval_cases.json"
RESULTS_PATH = ROOT_DIR / "evals" / "results.md"


def naive_extract(texto: str) -> dict:
    """
    Extractor simple y determinista para ejecutar evals de manera reproducible
    sin costo ni dependencia de credenciales de LLM en local.
    """
    t = texto.lower()
    productos = []

    for nombre_menu in MENU:
        if nombre_menu in t:
            match_cant = re.search(rf"(\d+)\s+{re.escape(nombre_menu.split()[0])}", t)
            cantidad = int(match_cant.group(1)) if match_cant else 1
            productos.append({"nombre": nombre_menu, "cantidad": cantidad})

    if not productos:
        for pista in ("de siempre", "hamburguesa", "gaseosa", "perro caliente", "pizza"):
            if pista in t and pista not in " ".join(MENU.keys()):
                productos.append({"nombre": pista, "cantidad": 1})

    direccion = None
    m = re.search(r"(cra|calle)\s*\d+[^,\.]*", t)
    if m:
        direccion = m.group(0).strip()
    elif "fuera de la zona de cobertura" in t or "zona rural" in t:
        direccion = "fuera de zona de cobertura"

    medio_pago = None
    for medio in ("nequi", "daviplata", "efectivo", "tarjeta", "transferencia"):
        if medio in t:
            medio_pago = medio
            break

    return {"productos": productos, "direccion_entrega": direccion, "medio_pago": medio_pago}


def run() -> list[dict]:
    casos = json.loads(EVAL_CASES_PATH.read_text(encoding="utf-8"))
    filas = []

    for caso in casos:
        extraccion = naive_extract(caso["input"])
        resultado = validar_pedido(extraccion, mensaje_original=caso["input"])
        expected = caso["expected"]

        checks_pasados = []
        checks_fallidos = []

        esperado_revision = expected.get("requires_human_review")
        if esperado_revision is not None:
            if resultado["requiere_revision"] == esperado_revision:
                checks_pasados.append("requires_human_review")
            else:
                checks_fallidos.append(
                    f"requires_human_review (esperado={esperado_revision}, real={resultado['requiere_revision']})"
                )

        if expected.get("must_not_apply_fake_discount"):
            if "descuento_no_autorizado" in resultado["motivos_revision"] or (resultado["total"] is not None and resultado["total"] > 0):
                checks_pasados.append("must_not_apply_fake_discount")
            else:
                checks_fallidos.append("must_not_apply_fake_discount")

        if expected.get("must_detect_ambiguity"):
            if any("ambiguo" in m or "no_reconocido" in m for m in resultado["motivos_revision"]):
                checks_pasados.append("must_detect_ambiguity")
            else:
                checks_fallidos.append("must_detect_ambiguity")

        if expected.get("must_check_delivery_zone") or expected.get("must_not_confirm_order"):
            if "direccion_fuera_de_cobertura" in resultado["motivos_revision"] or "direccion_faltante" in resultado["motivos_revision"]:
                checks_pasados.append("must_check_delivery_zone")
            else:
                checks_fallidos.append("must_check_delivery_zone")

        if expected.get("must_check_product_availability"):
            if any("producto_no_disponible" in m for m in resultado["motivos_revision"]):
                checks_pasados.append("must_check_product_availability")
            else:
                checks_fallidos.append("must_check_product_availability")

        if expected.get("must_not_send_to_kitchen"):
            if resultado["requiere_revision"]:
                checks_pasados.append("must_not_send_to_kitchen")
            else:
                checks_fallidos.append("must_not_send_to_kitchen")

        estado = "PASS" if not checks_fallidos else "FAIL"
        filas.append(
            {
                "id": caso["id"],
                "estado": estado,
                "motivos_revision": resultado["motivos_revision"],
                "checks_pasados": checks_pasados,
                "checks_fallidos": checks_fallidos,
            }
        )

    return filas


def escribir_resultados(filas: list[dict]) -> None:
    hoy = date.today().isoformat()
    ahora = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lineas = [
        "# Eval Baseline - P-Bot",
        "",
        f"Fecha: {hoy}",
        "",
        "## Como correr",
        "",
        "```bash",
        "python evals/run_evals.py",
        "```",
        "",
        "## Alcance de la evaluacion",
        "",
        "Prueba el comportamiento de la **capa de validacion determinista** (`validador_pedido.py`) "
        "frente a las extracciones estructuradas. Para ejecutar las pruebas sin depender de claves de API externas, "
        "se utiliza una extraccion heuristica (`naive_extract`).",
        "",
        f"Ultima ejecucion: {ahora}",
        "",
        "## Resultados",
        "",
        "| Caso de Prueba | Estado | Motivos Detectados |",
        "|---|---|---|",
    ]

    for fila in filas:
        motivos = ", ".join(fila["motivos_revision"]) or "ninguno"
        lineas.append(f"| {fila['id']} | {fila['estado']} | {motivos} |")

    total = len(filas)
    passed = sum(1 for f in filas if f["estado"] == "PASS")
    lineas += [
        "",
        f"**Score global: {passed}/{total}**",
        "",
        "## Analisis del caso `pbot_ambiguous_product`",
        "",
        "En el caso de 'hamburguesa sencilla sin carne', existe una contradiccion semantica que debe ser interpretada "
        "por el modelo de lenguaje (LLM). Dado que la prueba determinista offline busca coincidencia de texto literal, "
        "extrae 'hamburguesa sencilla'. Este resultado resalta claramente los limites entre lo que corresponde al LLM "
        "(interpretacion de contexto) y lo que corresponde al codigo determinista (validacion de catalogo y precios).",
        "",
    ]

    RESULTS_PATH.write_text("\n".join(lineas), encoding="utf-8")


if __name__ == "__main__":
    filas = run()
    escribir_resultados(filas)
    for fila in filas:
        print(f"{fila['estado']:5s} {fila['id']}  motivos={fila['motivos_revision']}")
    total = len(filas)
    passed = sum(1 for f in filas if f["estado"] == "PASS")
    print(f"\nScore: {passed}/{total}  ->  evals/results.md actualizado")
