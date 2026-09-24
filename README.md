# MATI — Matemática Aplicada a las Tecnologías de la Información

Notebooks y entregas de la asignatura MATI (Grado en Ingeniería Informática, Universidad de Sevilla, curso 2026/2027): teoría de grafos, álgebra discreta, caminos mínimos y flujos en redes.

```
MATI/
├── notebooks/          un notebook por entrega + plantilla y utilidades compartidas
├── scripts/            herramientas del proyecto (exportador de entregas)
├── entregas/           PDFs generados, listos para subir a la plataforma
├── exportar.ps1        atajo para lanzar el exportador sin activar el .venv
├── CLAUDE.md           convenciones del proyecto (contexto para Claude Code)
└── GUIA_USO.md         manual de consulta: entorno, flujo de trabajo, cheat sheet
```

Para el día a día (activar el entorno, arrancar Jupyter Lab, estructura de un ejercicio), la referencia es **`GUIA_USO.md`**. Este README cubre solo cómo preparar el PDF de una entrega.

---

## Generar el PDF de una entrega

El script `scripts/exportar_entrega.py` convierte un notebook en el PDF que se sube a la plataforma, **con todas las celdas de código ya ejecutadas y sus resultados visibles** (texto y figuras).

### Uso

Desde la raíz del proyecto, sin necesidad de activar el entorno virtual:

```powershell
.\exportar.ps1 notebooks\00_practica-0.ipynb
```

O, si ya tienes el `.venv` activado y prefieres llamar al script directamente:

```powershell
python scripts/exportar_entrega.py notebooks/00_practica-0.ipynb
```

El PDF aparece en `entregas\` con el mismo nombre que el notebook (`entregas\00_practica-0.pdf`). Tarda unos minutos, porque lo primero que hace es ejecutar el notebook entero.

### Opciones

| Opción | Para qué sirve |
|---|---|
| `--sin-ejecutar` | No ejecuta el notebook; aprovecha las salidas ya guardadas. Útil si acabas de ejecutarlo en Jupyter Lab, o si alguna celda tarda mucho. |
| `--mantener-html` | Deja también el `.html` intermedio junto al PDF (se puede abrir en el navegador). |
| `-s`, `--salida CARPETA` | Carpeta de destino, por si no quieres `entregas\`. |
| `--timeout SEGUNDOS` | Tiempo máximo por celda al ejecutar (por defecto 1200). |

```powershell
# Ejemplo: exportar sin volver a ejecutar y conservando el HTML
.\exportar.ps1 notebooks\00_practica-0.ipynb --sin-ejecutar --mantener-html
```

### Qué hace por dentro

1. **Ejecuta** el notebook de arriba a abajo (`nbconvert --execute --inplace`) y guarda las salidas dentro del propio `.ipynb`, así que **el notebook que entregas ya lleva los resultados** — no hace falta acordarse de *Restart Kernel and Run All* antes de subirlo.
2. **Exporta a HTML** con las figuras incrustadas en el propio fichero (sin carpeta de imágenes suelta).
3. **Imprime ese HTML a PDF** con Chrome en modo headless.

Hay dos detalles no obvios que el script resuelve solo:

- **Las cajas de color.** Los bloques del notebook (📋 Enunciado, 📚 Teoría, 🧮 Resolución…) son `<div>` de HTML dentro de celdas Markdown. Jupyter Lab los pinta bien aunque tengan saltos de línea dentro, pero nbconvert no: parte el HTML en bloques y el `<div>` se cierra por su cuenta, y las cajas salen sin color. El script normaliza cada caja **sobre una copia temporal**, así que tu notebook se queda exactamente como lo escribiste.
- **Las fórmulas.** MathJax tipografía el LaTeX en el navegador, no en el HTML, así que la impresión espera a que termine antes de disparar el PDF.

### Requisitos

- El entorno virtual del proyecto (`.venv`) con las dependencias de `requirements.txt`; en particular `nbconvert`, que ya viene con Jupyter Lab.
- El kernel `mati-venv` registrado (ver `GUIA_USO.md` §1.2). El script usa el kernel que declare el notebook.
- **Chrome o Edge** instalado. El script los busca en las rutas habituales de Windows; si tienes el navegador en otro sitio, indícaselo con:
  ```powershell
  $env:CHROME = "D:\ruta\a\chrome.exe"
  ```
- **Conexión a internet** al exportar: MathJax se descarga de un CDN para componer las fórmulas. Sin red, el PDF saldría con el LaTeX en crudo (`$\alpha(G)$` en vez de tipografiado) — merece la pena echarle un vistazo al PDF antes de entregar.

> No se usa `jupyter nbconvert --to pdf` (necesita una instalación de LaTeX) ni `--to webpdf` (necesita Playwright): ninguno de los dos está en este equipo, y Chrome sí.

### Si algo falla

| Mensaje | Qué pasa |
|---|---|
| `no se encuentra Chrome ni Edge` | Define la variable de entorno `CHROME` con la ruta al ejecutable. |
| `nbconvert falló (--to notebook --execute ...)` | Una celda del notebook da error. Ábrelo en Jupyter Lab, ejecútalo a mano y corrige la celda; el script imprime el error completo. |
| `No se encuentra ...\.venv\Scripts\python.exe` | Falta el entorno virtual: ver `GUIA_USO.md` §1.1. |
| Las fórmulas salen como `$...$` | Se exportó sin conexión a internet. Vuelve a lanzarlo con red. |
