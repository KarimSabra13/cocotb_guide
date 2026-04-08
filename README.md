# Cocotb DV Guide

Repository for the actual Python guide code at the root, with `docs/` kept mostly local and out of Git.

This repository is intentionally scaffolded first. The real teaching code lives outside the ignored docs workspace, while the documentation workspace under `docs/` is treated as local authoring material.

The actual prose guide is still in skeleton mode. The real guide code stays outside `docs/`.

## Git Policy

- Guide code outside `docs/` is the real tracked course material.
- Inside `docs/`, Git should keep only generated final PDFs and README markdown files.
- LaTeX sources, figure specs, internal tooling code, and other authoring files under `docs/` stay local and ignored.

## Core choices

- Book layout: LuaLaTeX with KOMA-Script for a professional long-form document structure.
- Code presentation: `minted` plus `tcolorbox` for clean, publication-grade code blocks.
- Native TeX figures: TikZ, CircuitikZ, TikZ Timing, PGFPlots, and Bytefield.
- Python figure pipeline: Typer-based CLI with structured YAML specs, ready to evolve into FSM, timing, and schematic renderers.

## Repository layout

```text
docs/
  tracked in Git: final PDFs plus README markdown files
  ignored in Git: LaTeX sources, tooling, specs, and build intermediates
outside docs/ actual guide code lives here
```

## Local docs workflow

1. Keep your local authoring files inside `docs/`.
2. Compile the guide locally.
3. Commit only the final generated PDF from `docs/` plus markdown files you want to keep.

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
