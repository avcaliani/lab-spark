## Who & Why

Spark learning lab (Scala and PySpark) for a Python-first data engineer.

Prioritize clarity over cleverness. Be terse.

For Scala: assume strong PySpark intuition, little Scala syntax.
Anchor to PySpark analogues.

## Repo Layout

Read [`README.md`](README.md) first (file tree), then [`pocs/README.md`](pocs/README.md) (shared universe).

Each poc has its own README.

Stack: Java 21, Spark 4.1.1, Delta Lake 4.3.1.
Keep versions aligned across pocs.

**NEVER run Python or PySpark commands outside the virtual env.**
Use `uv run ...` from the folder that owns the `pyproject.toml`, or the project's container.

## Keep Docs Updated

If you spot incorrect or outdated docs or comments, alert the user and suggest the fix.
