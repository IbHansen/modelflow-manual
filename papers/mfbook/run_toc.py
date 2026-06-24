"""Run the notebooks listed in a Jupyter Book v1 _toc.yml, in parallel.

Only notebooks referenced by the table of contents are executed; any other
notebooks in the tree are ignored. Non-notebook entries (e.g. .md pages) in
the toc are skipped. Each notebook runs in its own folder.

Usage:
    python run_toc.py _toc.yml
    python run_toc.py path/to/_toc.yml -j 2
    python run_toc.py _toc.yml --inplace          # overwrite originals (book PNGs)
    python run_toc.py _toc.yml -j 1 --timeout 120 # find a hanging notebook

JB v1 _toc.yml is a nested structure of `root:` / `file:` entries under
`parts` -> `chapters` -> `sections` (or, in the legacy format, a bare list of
`- file:` items). Paths are relative to the _toc.yml folder and carry no
extension; this script appends `.ipynb` and runs only entries that exist.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

# Force a non-interactive matplotlib backend so plt.show() can't pop a GUI
# window and block a worker forever. setdefault inherits into worker processes.
os.environ.setdefault("MPLBACKEND", "Agg")
# Marker notebooks can check to skip blocking calls (e.g. Dash app.run()).
os.environ.setdefault("PAPERMILL", "1")

import papermill as pm
import yaml


def collect_files(node) -> list[str]:
    """Recursively pull every `root:`/`file:` string out of a parsed _toc.yml."""
    found: list[str] = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key in ("root", "file") and isinstance(value, str):
                found.append(value)
            else:
                found.extend(collect_files(value))
    elif isinstance(node, list):
        for item in node:
            found.extend(collect_files(item))
    return found


def resolve_notebooks(toc_path: Path) -> tuple[list[Path], list[str]]:
    """Return (existing notebooks, skipped non-notebook entries) from a _toc.yml."""
    base = toc_path.resolve().parent
    with open(toc_path, encoding="utf-8") as fh:
        toc = yaml.safe_load(fh)

    notebooks: list[Path] = []
    skipped: list[str] = []
    seen: set[Path] = set()
    for ref in collect_files(toc):
        # toc entries are extensionless; an explicit extension is honoured too.
        candidate = base / ref
        nb = candidate if candidate.suffix == ".ipynb" else candidate.with_suffix(".ipynb")
        nb = nb.resolve()
        if nb.is_file():
            if nb not in seen:
                seen.add(nb)
                notebooks.append(nb)
        else:
            skipped.append(ref)
    return notebooks, skipped


def run(nb: str, inplace: bool, timeout: int | None) -> str:
    """Execute one notebook in its own folder; runs in a worker process."""
    src = Path(nb)
    out = src if inplace else src.with_suffix(".out.ipynb")
    print(f"START {nb}", flush=True)
    pm.execute_notebook(
        str(src), str(out),
        kernel_name="python3",
        cwd=str(src.parent),
        execution_timeout=timeout,   # seconds per cell; raises on a stuck cell
        progress_bar=False,          # tqdm bars from parallel workers interleave; suppress them
    )
    return nb


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("toc", help="path to the Jupyter Book v1 _toc.yml")
    parser.add_argument("-j", "--jobs", type=int, default=4, help="max concurrent notebooks")
    parser.add_argument("--inplace", action="store_true",
                        help="overwrite the source notebooks (e.g. to refresh book PNG outputs)")
    parser.add_argument("--timeout", type=int, default=None,
                        help="per-cell execution timeout in seconds; a stuck cell FAILs "
                             "instead of hanging the whole run (default: no limit)")
    args = parser.parse_args()

    toc_path = Path(args.toc)
    if not toc_path.is_file():
        print(f"No such _toc file: {toc_path}")
        return 1

    notebooks, skipped = resolve_notebooks(toc_path)
    if skipped:
        print(f"Skipping {len(skipped)} non-notebook toc entr(y/ies): {', '.join(skipped)}")
    if not notebooks:
        print("No notebooks resolved from the toc.")
        return 1

    print(f"Running {len(notebooks)} notebook(s) from {toc_path} with up to {args.jobs} workers:")
    for nb in notebooks:
        print(f"  - {nb}")

    failures: dict[str, str] = {}
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=args.jobs) as ex:
        futures = {ex.submit(run, str(nb), args.inplace, args.timeout): str(nb) for nb in notebooks}
        for fut in as_completed(futures):
            nb = futures[fut]
            try:
                fut.result()
                print(f"OK   {nb}")
            except Exception as exc:  # noqa: BLE001 - report, keep going
                failures[nb] = str(exc)
                print(f"FAIL {nb}: {exc}")

    elapsed = time.perf_counter() - start
    mins, secs = divmod(elapsed, 60)
    print(f"\n{len(notebooks) - len(failures)}/{len(notebooks)} succeeded "
          f"in {int(mins)}m {secs:.1f}s ({elapsed:.1f}s).")
    if failures:
        print("Failed:")
        for nb, err in failures.items():
            print(f"  {nb}: {err.splitlines()[-1] if err else ''}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
