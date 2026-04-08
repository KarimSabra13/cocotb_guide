from __future__ import annotations

from cocotb_dv_guide.diagramgen.models import DiagramSpec
from cocotb_dv_guide.diagramgen.renderers.fsm import render as render_fsm
from cocotb_dv_guide.diagramgen.renderers.schematic import render as render_schematic
from cocotb_dv_guide.diagramgen.renderers.timing import render as render_timing

RENDERERS = {
    "fsm": render_fsm,
    "schematic": render_schematic,
    "timing": render_timing,
}


def available_kinds() -> list[str]:
    return sorted(RENDERERS)


def render_diagram(spec: DiagramSpec) -> str:
    return RENDERERS[spec.kind](spec)
