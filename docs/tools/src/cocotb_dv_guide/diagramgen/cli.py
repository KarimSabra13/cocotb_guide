from __future__ import annotations

import json
from pathlib import Path

import typer
import yaml
from rich.console import Console

from cocotb_dv_guide.diagramgen.models import DiagramSpec
from cocotb_dv_guide.diagramgen.renderers import available_kinds, render_diagram

app = typer.Typer(add_completion=False, no_args_is_help=True)
console = Console()

TEMPLATES = {
    "fsm": """kind: fsm\ntitle: Example FSM\nnotes:\n  - Replace this template with the real state machine.\nstates:\n  - IDLE\n  - ACTIVE\ntransitions:\n  - source: IDLE\n    target: ACTIVE\n    label: start\n""",
    "schematic": """kind: schematic\ntitle: Example Schematic\nnotes:\n  - Replace this template with the real block diagram.\nblocks:\n  - name: DUT\n    type: dut\nnets: []\n""",
    "timing": """kind: timing\ntitle: Example Timing Diagram\nnotes:\n  - Replace this template with real waveforms.\nsignals:\n  clk: \"P...\"\nevents: []\n""",
}


def _load_spec(path: Path) -> DiagramSpec:
    text = path.read_text(encoding="utf-8")

    if path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        data = yaml.safe_load(text)

    if not isinstance(data, dict):
        raise typer.BadParameter(f"Spec file must contain a mapping: {path}")

    return DiagramSpec.from_mapping(data)


def _spec_files(directory: Path) -> list[Path]:
    matches = []
    for suffix in ("*.yaml", "*.yml", "*.json"):
        matches.extend(directory.rglob(suffix))
    return sorted(matches)


@app.command()
def render(
    spec: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    output: Path = typer.Argument(..., dir_okay=False),
) -> None:
    """Render one diagram spec into an SVG placeholder asset."""

    diagram = _load_spec(spec)
    svg = render_diagram(diagram)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")
    console.print(f"[green]wrote[/green] {output}")


@app.command()
def batch(
    specs_dir: Path = typer.Argument(..., exists=True, file_okay=False, readable=True),
    output_dir: Path = typer.Argument(..., file_okay=False),
) -> None:
    """Render every spec under a directory, preserving relative structure."""

    spec_paths = _spec_files(specs_dir)
    if not spec_paths:
        raise typer.BadParameter(f"No specs found under: {specs_dir}")

    for spec_path in spec_paths:
        relative_output = spec_path.relative_to(specs_dir).with_suffix(".svg")
        output_path = output_dir / relative_output
        diagram = _load_spec(spec_path)
        svg = render_diagram(diagram)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(svg, encoding="utf-8")
        console.print(f"[green]wrote[/green] {output_path}")


@app.command("init-spec")
def init_spec(
    kind: str = typer.Argument(..., help="One of: fsm, schematic, timing."),
    output: Path = typer.Argument(..., dir_okay=False),
    force: bool = typer.Option(False, "--force", help="Overwrite the output file if it exists."),
) -> None:
    """Write a starter YAML spec for a given diagram kind."""

    normalized_kind = kind.strip().lower()
    if normalized_kind not in TEMPLATES:
        raise typer.BadParameter(f"Unsupported kind: {kind}. Choose from {', '.join(available_kinds())}.")

    if output.exists() and not force:
        raise typer.BadParameter(f"Output already exists: {output}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(TEMPLATES[normalized_kind], encoding="utf-8")
    console.print(f"[green]initialized[/green] {output}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
