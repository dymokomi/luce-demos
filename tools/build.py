#!/usr/bin/env python3
"""Build native demos using public package exports and local dependencies."""
import argparse
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def build(demo, luce, base, output, opt=0):
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([str(luce.resolve()), "build", str(ROOT / "src" / (("ui_demo" if demo == "ui" else "sphere") + ".luc")),
                    "--native", "--opt", str(opt), "-o", str(output)],
                   env=dict(os.environ, LUCE_BASE=str(base.resolve())), check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("demo", choices=["ui", "sphere", "all"], nargs="?", default="all")
    parser.add_argument("--luce", type=Path, default=ROOT.parent / "luce/build/luce")
    parser.add_argument("--base", type=Path, default=Path(os.environ.get(
        "LUCE_BASE_COMPILER", ROOT.parent / "luce-base/build/luce-base")))
    parser.add_argument("--opt", type=int, choices=range(4), default=0)
    parser.add_argument("--output-directory", type=Path, default=ROOT / "build")
    args = parser.parse_args()
    for demo in (["ui", "sphere"] if args.demo == "all" else [args.demo]):
        build(demo, args.luce, args.base, args.output_directory / demo, args.opt)
