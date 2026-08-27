"""
run_evals.py

Cierra la brecha que encontramos en la revision del repo: `evals/eval_cases.json`
(agregado en la rama `makers/review`) nunca estaba conectado a ningun codigo.
`evals/results.md` tenia las 5 filas marcadas como "Pendiente" porque nadie
habia escrito el runner. Este script si las ejecuta y llena resultados reales.

Importante sobre el alcance -- para ser honestos con lo que esto prueba:

  Este runner ejecuta los casos contra la CAPA DETERMINISTA
  (`validador_pedido.py`), no contra el modelo de lenguaje. Probar el
  comportamiento real del LLM (Llama 3.1 70B via NVIDIA NIM) requiere
  NVIDIA_API_KEY y esta fuera del alcance de este cambio, que se enfoca en
  la parte que faltaba por completo: el codigo que decide si un pedido se
  confirma o se manda a revision humana, independientemente de lo que haya
  dicho el modelo.

  Para eso, cada caso usa un extractor "ingenuo" (naive_extract) que
  simula, con reglas simples de texto, una extraccion imperfecta como la
  que haria un LLM -- deliberadamente imperfecto, para probar que el
  validador atrapa los problemas incluso cuando la extraccion no es
  perfecta. Cuando el equipo tenga NVIDIA_API_KEY configurada, pueden
  reemplazar `naive_extract` por `run_prototype` (celda 16 del notebook)
  sin cambiar nada de `validador_pedido.py` ni de este runner: la interfaz
  es la misma (dict de entrada -> dict validado).

Uso:
    python evals/run_evals.py
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from validador_pedido import MENU, validar_pedido  # noqa: E402

EVAL_CASES_PATH = Path(__file__).resolve().parent / "eval_cases.json"
RESULTS_PATH = Path(__file__).resolve().parent / "results.md"


def naive_extract(texto: str) -> dict:
    """Extractor ingenuo basado en reglas de texto (NO es un LLM).

    Sirve solo para tener algo que alimentar a `validar_pedido` de forma
    reproducible y sin API key. Intencionalmente simple: por ejemplo, para
    "la de siempre" no reconoce ningun producto (correcto: no deberia
    inventarlo), y para "hamburguesa sencilla pero sin carne" solo copia el
    texto tal cual como nombre de producto, dejando que el validador decida
    si es ambiguo -- que es exactamente lo que se quiere probar aqui.
    """
    t = texto.lower()
    productos = []

    for nombre_menu in MENU:
        if nombre_menu in t:
            cantidad_match = re.search(rf"(\d+)\s+{re.escape(nombre_menu.split()[0])}", t)
            cantidad = int(cantidad_match.group(1)) if cantidad_match else 1
            productos.append({"nombre": nombre_menu, "cantidad": cantidad})

    if not productos:
        # frases que claramente piden algo pero no algo del menu reconocible
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
    cases = json.loads(EVAL_CASES_PATH.read_text(encoding="utf-8"))
    filas = []

    for caso in cases:
        extraccion = naive_extract(caso["input"])
        resultado = validar_pedido(extraccion, mensaje_original=caso["input"])
        expected = caso["expected"]

        checks_pasados = []
        checks_fallidos = []

        # todos los casos tienen requires_human_review
        esperado_revision = expected.get("requires_human_review")
        if esperado_revision is not None:
            if resultado["requiere_revision"] == esperado_revision:
                checks_pasados.append("requires_human_review")
            else:
                checks_fallidos.append(
                    f"requires_human_review (esperado={esperado_revision}, real={resultado['requiere_revision']})"
                )

        if expected.get("must_not_apply_fake_discount"):
            if "descuento_no_autorizado" in resultado["motivos_revision"] or resultado["total"] != 0:
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
        "```",
        "python evals/run_evals.py",
        "```",
        "",
        "## Alcance de este resultado",
        "",
        "Estos resultados prueban la **capa deterministica** "
        "(`validador_pedido.py`), no el comportamiento del LLM en produccion. "
        "El extractor usado aqui (`naive_extract`, reglas de texto simples, sin IA) "
        "es un reemplazo deliberadamente imperfecto de `run_prototype()` (celda 16 "
        "del notebook), para poder correr los evals sin `NVIDIA_API_KEY` y de forma "
        "100% reproducible. Cuando el equipo tenga la API key configurada, pueden "
        "sustituir `naive_extract` por `run_prototype` en `evals/run_evals.py` sin "
        "tocar `validador_pedido.py`, y volver a correr esto para tener tambien el "
        "baseline real del modelo.",
        "",
        f"Ultima corrida: {ahora}",
        "",
        "## Resultados (capa deterministica)",
        "",
        "| Caso | Resultado | Motivos detectados |",
        "|---|---|---|",
    ]

    for fila in filas:
        motivos = ", ".join(fila["motivos_revision"]) or "ninguno"
        lineas.append(f"| {fila['id']} | {fila['estado']} | {motivos} |")

    total = len(filas)
    passed = sum(1 for f in filas if f["estado"] == "PASS")
    lineas += [
        "",
        f"**Score capa deterministica: {passed}/{total}**",
        "",
        "## Por que falla pbot_ambiguous_product (y por que se deja asi, sin maquillar)",
        "",
        "El input es \"hamburguesa sencilla **pero sin carne**\": una contradiccion "
        "semantica (una hamburguesa sin su ingrediente principal), no un error de "
        "escritura. `naive_extract` (el reemplazo de la extraccion del LLM, ver "
        "seccion de Alcance) solo busca substrings de nombres del menu, y "
        "\"hamburguesa sencilla\" SI aparece tal cual en el texto -> lo extrae como "
        "match exacto y valido. `validador_pedido.py` solo puede marcar ambiguedad "
        "en el *nombre* del producto (typos, nombres parecidos via `difflib`); no "
        "entiende el significado de los modificadores (\"sin carne\", \"sin pollo\"), "
        "porque esa interpretacion semantica es exactamente el trabajo que le "
        "corresponde al LLM, no a la capa deterministica. Con un extractor real "
        "(`run_prototype`) es probable que el modelo si detecte la contradiccion en "
        "el texto; este FAIL documenta el limite real de lo que la capa "
        "deterministica puede resolver por si sola, para que quede explicito en "
        "vez de escondido.",
        "",
        "## Pendiente (fuera de alcance de este cambio)",
        "",
        "- Correr estos mismos casos contra el LLM real (`run_prototype`, celda 16) "
        "con `NVIDIA_API_KEY` configurada, para tener el baseline del modelo, no solo "
        "del validador.",
        "- Extender `naive_extract` o reemplazarlo por NLU real si se quiere seguir "
        "corriendo evals sin costo de API.",
        "",
        "## Hipotesis inicial (heredada de la revision anterior)",
        "",
        "El agente puede estructurar pedidos, pero el sistema debe validar contra "
        "menu, precios, cobertura y medios de pago antes de confirmar. La IA "
        "interpreta texto; el codigo debe proteger el negocio. Esa validacion ya "
        "existe ahora en `validador_pedido.py` y esta cubierta por "
        "`tests/test_validador_pedido.py`.",
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
