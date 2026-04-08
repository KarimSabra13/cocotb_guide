# Cocotb DV Guide

Repository for the actual Python guide code at the root and the guide-writing toolchain under `docs/`.

This repository is intentionally scaffolded first. The structure for writing the guide is ready, while the real teaching code lives at the repository root.

The actual prose guide is still in skeleton mode. The root-level Python folders are the real guide code, starting with `Python_Fundementals/`.

## Repository boundaries

- Real guide code: root-level Python folders such as `Python_Fundementals/`, plus future root-level topic folders.
- Real guide document content: `docs/chapters/`, `docs/frontmatter/`, `docs/config/`, and the final tracked PDF under `docs/build/`.
- Internal setup and authoring tools only: `docs/tools/`, `.vscode/`, and figure spec helpers under `docs/figures/specs/`.

If a file only exists to help write, draw, render, lint, or build the guide, treat it as tooling. If a file is part of the guide itself, a cocotb example, or the final PDF artifact, treat it as actual project content.

## Core choices

- Book layout: LuaLaTeX with KOMA-Script for a professional long-form document structure.
- Code presentation: `minted` plus `tcolorbox` for clean, publication-grade code blocks.
- Native TeX figures: TikZ, CircuitikZ, TikZ Timing, PGFPlots, and Bytefield.
- Python figure pipeline: Typer-based CLI with structured YAML specs, ready to evolve into FSM, timing, and schematic renderers.

## Repository layout

```text
docs/
  bibliography/      BibLaTeX database
  build/             Build area; only final PDF is meant to be tracked
  chapters/          Chapter shells only
  config/            TeX metadata, packages, theme, and macros
  figures/
    generated/       Generated assets, ignored except for directory marker
    specs/           YAML source specs for the Python diagram pipeline
  frontmatter/       Title page and future front matter
  latexmkrc          LaTeX build configuration
  main.tex           Master document
  tools/
    pyproject.toml   Internal Python tooling package config
    src/             Internal diagram and authoring tooling only
    tests/           Internal smoke tests for tooling
Python_Fundementals/ Actual guide code already started at the repo root
```

## First bootstrap

1. Create and activate a Python environment.
2. Install the doc tooling with `python -m pip install -e ./docs/tools[dev]`.
3. Ensure TeX Live or MiKTeX provides `latexmk`, `lualatex`, `biber`, `minted`, `tikz`, `circuitikz`, `pgfplots`, `tikz-timing`, and `bytefield`.
4. Use the VS Code tasks or run `latexmk` from the repository root.

## Current status

1. Chapter prose: not started
2. Root-level Python guide code: started
3. Final PDF: not generated yet
4. Tooling and repo preparation: ready

## Planned book flow

1. Verification context and why cocotb matters
2. Cocotb fundamentals and coroutine model
3. Testbench architecture: drivers, monitors, scoreboards, and reference models
4. Clocks, resets, synchronization, and timing control
5. Randomization, coverage, and stimulus strategy
6. Debug, waveforms, and failure analysis
7. Regression, automation, and CI
8. Real DV case studies and reusable project patterns
