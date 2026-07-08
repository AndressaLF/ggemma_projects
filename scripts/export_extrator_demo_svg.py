"""Exporta tabela demo do extrator como SVG para a vitrine."""
from __future__ import annotations

import sys
from pathlib import Path

EXTRATOR_SRC = Path(__file__).resolve().parents[2] / "extrator_info_files" / "src"
sys.path.insert(0, str(EXTRATOR_SRC))

from rich.console import Console  # noqa: E402

import extrator.reporter as reporter  # noqa: E402
from extrator.reporter import print_overview, print_results_table  # noqa: E402
from extrator.scanner import scan_folder  # noqa: E402

DEMO = EXTRATOR_SRC.parent / "banco_de_dados_treinamento" / "amostras_sinteticas"
OUT = Path(__file__).resolve().parents[1] / "docs" / "assets" / "extrator_demo_tabela.svg"


def main() -> None:
    console = Console(record=True, width=130, force_terminal=True)
    reporter.console = console

    result = scan_folder(DEMO, recursive=False)
    print_overview(result)
    print_results_table(result)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    console.save_svg(str(OUT), title="extrator_info_files — demo")
    print(f"Salvo: {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
