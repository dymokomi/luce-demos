#!/usr/bin/env python3
"""Compile real demos, exercise their handlers, and check clean build output."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--gui', action='store_true')
parser.add_argument('--opt', type=int, choices=range(4))
args = parser.parse_args()
base = ROOT.parent / 'luce-base/build/luce-base'
luce = ROOT.parent / 'luce/build/luce'
env = dict(os.environ, LUCE_BASE=str(base), MTL_DEBUG_LAYER='1', MTL_SHADER_VALIDATION='1')
with tempfile.TemporaryDirectory(prefix='luce-demos-tests-') as temporary:
    work = Path(temporary)
    output = work / 'output'
    scratch = work / 'scratch'
    scratch.mkdir()
    env['TMPDIR'] = str(scratch)
    def clean():
        # xcrun caches SDK discovery in TMPDIR on macOS. It is host tool state,
        # while every compiler-owned workspace/source must be removed.
        remaining = [p for p in scratch.iterdir() if p.name != 'xcrun_db']
        assert not remaining, f'build retained scratch files: {remaining}'

    for level in ([args.opt] if args.opt is not None else range(4)):
        subprocess.run(['python3', str(ROOT / 'tools/build.py'), '--opt', str(level), '--output-directory', str(output)], check=True, env=env, timeout=300)
        assert sorted(p.name for p in output.iterdir()) == ['sphere', 'ui']
        clean()
        if args.gui:
            for name in ['ui', 'sphere']:
                subprocess.run([str(output / name), '--smoke'], check=True, env=env, timeout=60)
        binary = work / 'interaction'
        subprocess.run([str(luce), 'build', str(ROOT / 'src/tests/interaction.luc'), '--native', '--opt', str(level), '-o', str(binary)], check=True, env=env, timeout=180)
        subprocess.run([str(binary)], check=True, env=env, timeout=30)
        clean()
    invalid = work / 'invalid.luc'
    invalid.write_text('pub func main(arguments: list[str]) -> int!:\n    return absent\n')
    result = subprocess.run([str(luce), 'build', str(invalid), '-o', str(output / 'invalid')], capture_output=True, text=True, env=env, timeout=60)
    assert result.returncode != 0 and 'absent' in result.stderr, result
    assert sorted(p.name for p in output.iterdir()) == ['sphere', 'ui']
    clean()
print('PASS native demo builds, application interactions and clean output')
