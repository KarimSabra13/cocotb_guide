from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

DiagramKind = Literal["fsm", "timing", "schematic"]


class DiagramSpec(BaseModel):
    kind: DiagramKind
    title: str = "Untitled Diagram"
    notes: list[str] = Field(default_factory=list)
    payload: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "DiagramSpec":
        if "kind" not in data:
            raise ValueError("Diagram spec is missing a 'kind' field.")

        payload = dict(data)
        kind = payload.pop("kind")
        title = payload.pop("title", "Untitled Diagram")
        notes = payload.pop("notes", [])
        return cls(kind=kind, title=title, notes=notes, payload=payload)
