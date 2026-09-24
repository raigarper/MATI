<#
.SYNOPSIS
    Genera el PDF entregable de un notebook de MATI.

.DESCRIPTION
    Atajo para no tener que activar el entorno virtual: llama a
    scripts\exportar_entrega.py con el Python del .venv del proyecto.
    Los parámetros que le pases se reenvían tal cual al script.

.EXAMPLE
    .\exportar.ps1 notebooks\00_practica-0.ipynb

.EXAMPLE
    .\exportar.ps1 notebooks\00_practica-0.ipynb --sin-ejecutar --mantener-html
#>

$ErrorActionPreference = "Stop"

$raiz   = $PSScriptRoot
$python = Join-Path $raiz ".venv\Scripts\python.exe"
$script = Join-Path $raiz "scripts\exportar_entrega.py"

if (-not (Test-Path $python)) {
    Write-Error "No se encuentra $python. ¿Está creado el entorno virtual? (ver GUIA_USO.md §1.1)"
}

& $python $script @args
exit $LASTEXITCODE
