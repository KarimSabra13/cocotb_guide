# Docs Tooling

This folder contains only the internal tooling used to write, render, and validate the guide.

Nothing here is chapter content or final teaching material.

This README stays tracked, but the code and config files in this folder are now ignored by Git as part of the docs policy.

Contents:

- `src/` for the internal Python authoring package
- `tests/` for tooling smoke tests
- `pyproject.toml` for tooling dependencies and commands

Install with `python -m pip install -e ./docs/tools[dev]` from the repository root.
