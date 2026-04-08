from __future__ import annotations

from cocotb_dv_guide.diagramgen.models import DiagramSpec
from cocotb_dv_guide.diagramgen.renderers.base import build_placeholder_svg


def render(spec: DiagramSpec) -> str:
    states = spec.payload.get("states", [])
    transitions = spec.payload.get("transitions", [])
    highlights = [
        "Target backend: Graphviz or TikZ automata layout.",
        f"States declared: {len(states)}.",
        f"Transitions declared: {len(transitions)}.",
    ]

    if spec.notes:
        highlights.append(f"Spec notes captured: {len(spec.notes)}.")

    return build_placeholder_svg(title=spec.title, kind=spec.kind, highlights=highlights)
