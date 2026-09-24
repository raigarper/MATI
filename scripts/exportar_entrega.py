# -*- coding: utf-8 -*-
"""Convierte un notebook de MATI en el PDF que se entrega en la plataforma.

Uso típico (con el .venv activado, desde la raíz del proyecto):

    python scripts/exportar_entrega.py notebooks/00_practica-0.ipynb

Qué hace, en orden:
  1. Ejecuta el notebook de arriba a abajo y guarda las salidas dentro del
     propio .ipynb (así el notebook que entregas ya lleva los resultados).
  2. Lo exporta a HTML con las figuras incrustadas en el propio fichero.
  3. Imprime ese HTML a PDF con Chrome en modo headless.

Por qué no se usa `jupyter nbconvert --to pdf`: esa vía necesita una
instalación de LaTeX, y `--to webpdf` necesita Playwright. Ninguna de las dos
está en este equipo, y Chrome sí.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Sitios donde suele estar Chrome en Windows (se puede forzar con la variable
# de entorno CHROME). Edge sirve igual: es el mismo motor.
NAVEGADORES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def encontrar_navegador() -> str:
    """Devuelve la ruta del navegador con el que imprimir el PDF."""
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    for ruta in NAVEGADORES:
        if Path(ruta).exists():
            return ruta
    for nombre in ("chrome", "msedge"):
        encontrado = shutil.which(nombre)
        if encontrado:
            return encontrado
    raise SystemExit(
        "ERROR: no se encuentra Chrome ni Edge.\n"
        "       Indica la ruta a mano con la variable de entorno CHROME, p. ej.:\n"
        '       $env:CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"'
    )


def nbconvert(*args: str) -> None:
    """Llama a nbconvert con el mismo Python que ejecuta este script."""
    orden = [sys.executable, "-m", "nbconvert", *args]
    resultado = subprocess.run(orden, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if resultado.returncode != 0:
        print(resultado.stdout)
        print(resultado.stderr, file=sys.stderr)
        raise SystemExit(f"ERROR: nbconvert falló ({' '.join(args)})")


def normalizar_cajas(origen: Path, destino: Path) -> int:
    """Deja cada caja de color <div> en una sola línea, sobre una COPIA.

    Los bloques del notebook (📋 Enunciado, 📚 Teoría, 🧮 Resolución...) son
    `<div>` de HTML dentro de celdas Markdown. Jupyter Lab los pinta bien
    aunque tengan saltos de línea dentro, pero nbconvert no: parte el HTML en
    bloques, cierra el `<div>` por su cuenta y el resultado sale sin caja.
    Como es un problema solo de exportación, se arregla en una copia temporal
    y el notebook original se queda tal cual lo escribiste.
    """
    nb = json.loads(origen.read_text(encoding="utf-8"))
    arregladas = 0
    for celda in nb["cells"]:
        if celda["cell_type"] != "markdown":
            continue
        texto = "".join(celda["source"])
        if "<div style=" not in texto:
            continue
        ini = texto.index("<div style=")
        fin = texto.rindex("</div>") + len("</div>")
        caja = re.sub(r"\s*\n\s*", " ", texto[ini:fin])
        celda["source"] = [texto[:ini] + caja + texto[fin:]]
        arregladas += 1
    destino.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    return arregladas


def paginas_del_pdf(pdf: Path) -> int:
    """Cuenta las páginas del PDF sin depender de librerías externas."""
    return len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes()))


def main() -> None:
    # Los mensajes llevan acentos y emojis: evita que la consola los rechace.
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    parser = argparse.ArgumentParser(
        description="Genera el PDF entregable de un notebook de MATI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo:\n  python scripts/exportar_entrega.py notebooks/00_practica-0.ipynb",
    )
    parser.add_argument("notebook", type=Path, help="notebook a exportar (.ipynb)")
    parser.add_argument("-s", "--salida", type=Path, default=Path("entregas"),
                        help="carpeta donde dejar el PDF (por defecto: entregas/)")
    parser.add_argument("--sin-ejecutar", action="store_true",
                        help="no ejecuta el notebook; usa las salidas que ya tenga guardadas")
    parser.add_argument("--mantener-html", action="store_true",
                        help="conserva también el .html intermedio junto al PDF")
    parser.add_argument("--timeout", type=int, default=1200,
                        help="segundos máximos por celda al ejecutar (por defecto: 1200)")
    args = parser.parse_args()

    notebook = args.notebook.resolve()
    if not notebook.exists():
        raise SystemExit(f"ERROR: no existe el notebook {notebook}")
    if notebook.suffix != ".ipynb":
        raise SystemExit(f"ERROR: {notebook.name} no es un notebook .ipynb")

    salida = args.salida.resolve()
    salida.mkdir(parents=True, exist_ok=True)
    nombre = notebook.stem
    navegador = encontrar_navegador()

    # --- 1. Ejecutar el notebook y guardar las salidas dentro del .ipynb ---
    if args.sin_ejecutar:
        print("[1/3] Ejecución omitida (--sin-ejecutar)")
    else:
        print(f"[1/3] Ejecutando {notebook.name} ... (puede tardar unos minutos)")
        nbconvert("--to", "notebook", "--execute", "--inplace",
                  f"--ExecutePreprocessor.timeout={args.timeout}", str(notebook))

    # --- 2. Exportar a HTML, con las cajas de color ya normalizadas ---
    print("[2/3] Exportando a HTML ...")
    with tempfile.TemporaryDirectory() as tmp:
        copia = Path(tmp) / notebook.name
        cajas = normalizar_cajas(notebook, copia)
        nbconvert("--to", "html", "--embed-images",
                  "--output-dir", str(salida), "--output", nombre, str(copia))
    html = salida / f"{nombre}.html"
    print(f"      {cajas} cajas de color normalizadas para la exportación")

    # --- 3. Imprimir el HTML a PDF con el navegador ---
    print("[3/3] Imprimiendo a PDF ...")
    pdf = salida / f"{nombre}.pdf"
    subprocess.run(
        [navegador, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         # Margen para que MathJax (que se descarga de internet) acabe de
         # componer las fórmulas antes de que se dispare la impresión.
         "--virtual-time-budget=30000", "--run-all-compositor-stages-before-draw",
         f"--print-to-pdf={pdf}", html.resolve().as_uri()],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if not pdf.exists():
        raise SystemExit("ERROR: el navegador no ha generado el PDF")

    if not args.mantener_html:
        html.unlink()

    print()
    print(f"PDF listo: {pdf}")
    print(f"           {paginas_del_pdf(pdf)} páginas, {pdf.stat().st_size / 1024:.0f} KB")
    print("Revisa que las fórmulas salgan tipografiadas y no como $...$ (hace falta")
    print("conexión a internet: MathJax se descarga de un CDN al componer la página).")


if __name__ == "__main__":
    main()
