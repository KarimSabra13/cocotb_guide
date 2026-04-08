from __future__ import annotations

import sys
from pathlib import Path

import yaml

TOOLS_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = TOOLS_ROOT.parent.parent
sys.path.insert(0, str(TOOLS_ROOT / "src"))

from cocotb_dv_guide.diagramgen.models import DiagramSpec


def test_all_template_specs_parse() -> None:
    spec_paths = sorted((REPO_ROOT / "docs" / "figures" / "specs").rglob("*.yaml"))
    assert spec_paths

    for spec_path in spec_paths:
        data = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
        spec = DiagramSpec.from_mapping(data)
        assert spec.kind in {"fsm", "schematic", "timing"}
        assert spec.title
