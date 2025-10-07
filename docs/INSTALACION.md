# Instalación y Ejecución

## Requisitos
- Python 3.10+ (probado con 3.11), git.
- Windows: PowerShell recomendado. (Opcional) Extensión Mermaid para visualizar el diagrama.

## Pasos
1. Crear entorno virtual y activar:
   - `python -m venv .venv`
   - `./.venv/Scripts/Activate.ps1`
2. Instalar en modo editable:
   - `pip install -e .`
3. Ejecutar episodio de simulación:
   - `python -m horizonte.cli` o `horizonte`
4. Revisar telemetría en `logs/`.

## Dependencias Opcionales
- TDA (Gudhi/ripser) para topología persistente avanzada.
- scikit‑learn, scipy, networkx (incluidas en pyproject).

