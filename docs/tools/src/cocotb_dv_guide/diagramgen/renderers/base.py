from __future__ import annotations

from html import escape

from cocotb_dv_guide.diagramgen.styles import CANVAS_HEIGHT, CANVAS_WIDTH, FONT_STACK, MONO_STACK, PALETTE


def build_placeholder_svg(*, title: str, kind: str, highlights: list[str]) -> str:
    escaped_title = escape(title)
    escaped_kind = escape(kind.upper())
    item_markup = []

    for index, item in enumerate(highlights, start=1):
        y = 318 + (index - 1) * 86
        item_markup.append(
            f"""
    <circle cx=\"168\" cy=\"{y}\" r=\"8\" fill=\"{PALETTE['warm']}\" />
    <text x=\"196\" y=\"{y + 8}\" fill=\"{PALETTE['ink']}\" font-family=\"{FONT_STACK}\" font-size=\"30\">{escape(item)}</text>"""
        )

    items = "\n".join(item_markup)

    return f"""<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{CANVAS_WIDTH}\" height=\"{CANVAS_HEIGHT}\" viewBox=\"0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}\">
  <defs>
    <linearGradient id=\"hero\" x1=\"0%\" x2=\"100%\" y1=\"0%\" y2=\"100%\">
      <stop offset=\"0%\" stop-color=\"{PALETTE['paper']}\" />
      <stop offset=\"100%\" stop-color=\"#FFFFFF\" />
    </linearGradient>
  </defs>

  <rect width=\"100%\" height=\"100%\" fill=\"url(#hero)\" />
  <rect x=\"44\" y=\"44\" width=\"1352\" height=\"812\" rx=\"26\" fill=\"none\" stroke=\"{PALETTE['accent']}\" stroke-width=\"8\" />
  <rect x=\"92\" y=\"96\" width=\"1256\" height=\"182\" rx=\"22\" fill=\"{PALETTE['panel']}\" stroke=\"{PALETTE['line']}\" stroke-width=\"2\" />
  <rect x=\"92\" y=\"316\" width=\"1256\" height=\"456\" rx=\"22\" fill=\"{PALETTE['panel']}\" stroke=\"{PALETTE['line']}\" stroke-width=\"2\" />

  <text x=\"120\" y=\"162\" fill=\"{PALETTE['accent']}\" font-family=\"{FONT_STACK}\" font-size=\"28\" font-weight=\"700\">PYTHON DIAGRAM PIPELINE</text>
  <text x=\"120\" y=\"224\" fill=\"{PALETTE['ink']}\" font-family=\"{FONT_STACK}\" font-size=\"52\" font-weight=\"700\">{escaped_title}</text>
  <text x=\"120\" y=\"262\" fill=\"{PALETTE['muted']}\" font-family=\"{MONO_STACK}\" font-size=\"24\">kind = {escaped_kind}</text>
  <text x=\"120\" y=\"356\" fill=\"{PALETTE['accent']}\" font-family=\"{FONT_STACK}\" font-size=\"30\" font-weight=\"700\">CURRENT SKELETON STATE</text>

  {items}

  <text x=\"120\" y=\"820\" fill=\"{PALETTE['muted']}\" font-family=\"{MONO_STACK}\" font-size=\"20\">Generated placeholder asset. Replace renderer internals with final layout logic chapter by chapter.</text>
</svg>
"""
