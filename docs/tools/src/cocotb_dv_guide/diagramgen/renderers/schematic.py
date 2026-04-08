from __future__ import annotations

from cocotb_dv_guide.diagramgen.models import DiagramSpec
from cocotb_dv_guide.diagramgen.renderers.base import build_placeholder_svg


def render(spec: DiagramSpec) -> str:
    blocks = spec.payload.get("blocks", [])
    nets = spec.payload.get("nets", [])
    highlights = [
        "Target backend: Schemdraw for polished block and signal schematics.",
        f"Blocks declared: {len(blocks)}.",
        f"Nets declared: {len(nets)}.",
    ]

    if spec.notes:
        highlights.append(f"Spec notes captured: {len(spec.notes)}.")

    return build_placeholder_svg(title=spec.title, kind=spec.kind, highlights=highlights)
