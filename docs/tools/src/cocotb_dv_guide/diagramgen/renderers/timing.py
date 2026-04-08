from __future__ import annotations

from cocotb_dv_guide.diagramgen.models import DiagramSpec
from cocotb_dv_guide.diagramgen.renderers.base import build_placeholder_svg


def render(spec: DiagramSpec) -> str:
    signals = spec.payload.get("signals", {})
    events = spec.payload.get("events", [])
    highlights = [
        "Target backend: WaveDrom-driven SVG timing diagrams.",
        f"Signals declared: {len(signals)}.",
        f"Events declared: {len(events)}.",
    ]

    if spec.notes:
        highlights.append(f"Spec notes captured: {len(spec.notes)}.")

    return build_placeholder_svg(title=spec.title, kind=spec.kind, highlights=highlights)
