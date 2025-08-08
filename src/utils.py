# Este módulo proporciona funciones auxiliares y utilitarias.
# Incluye herramientas simples para facilitar el desarrollo y la depuración.

from pathlib import Path


def debug_log(message: str) -> None:
    """Imprime un mensaje de depuración formateado."""
    print(f"DEBUG: {message}")


def ensure_dir(path: Path) -> None:
    """Crea el directorio especificado si aún no existe."""
    Path(path).mkdir(parents=True, exist_ok=True)

