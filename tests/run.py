#!/usr/bin/env python3
"""Compile real demos, exercise their handlers, and check clean build output."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile
import sys
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base', type=Path, default=ROOT.parent / ('luce-base/build/luce-base.exe' if os.name == 'nt' else 'luce-base/build/luce-base'))
parser.add_argument('--luce', type=Path, default=ROOT.parent / ('luce/build/luce.exe' if os.name == 'nt' else 'luce/build/luce'))
parser.add_argument('--gui', action='store_true')
parser.add_argument('--opt', type=int, choices=range(4))
args = parser.parse_args()
base = args.base.resolve()
luce = args.luce.resolve()
env = dict(os.environ, LUCE_BASE=str(base), MTL_DEBUG_LAYER='1', MTL_SHADER_VALIDATION='1')
with tempfile.TemporaryDirectory(prefix='luce-demos-tests-') as temporary:
    work = Path(temporary)
    output = work / 'output'
    scratch = work / 'scratch'
    scratch.mkdir()
    env['TMPDIR'] = str(scratch)
    if os.name == 'nt':
        env['TEMP'] = env['TMP'] = str(scratch)
    expected_outputs = ['sphere.exe', 'ui.exe'] if os.name == 'nt' else ['sphere', 'ui']
    def clean():
        # xcrun and Vulkan validation cache host tool state in the temp directory,
        # while every compiler-owned workspace/source must be removed.
        remaining = [p for p in scratch.iterdir() if p.name not in {'xcrun_db', 'shader_validation_cache.bin'}]
        assert not remaining, f'build retained scratch files: {remaining}'

    for level in ([args.opt] if args.opt is not None else range(4)):
        subprocess.run([sys.executable, str(ROOT / 'tools/build.py'), '--base', str(base), '--luce', str(luce), '--opt', str(level), '--output-directory', str(output)], check=True, env=env, timeout=300)
        assert sorted(p.name for p in output.iterdir()) == expected_outputs
        clean()
        if args.gui:
            for name in ['ui', 'sphere']:
                subprocess.run([str(output / name), '--smoke'], check=True, env=env, timeout=60)
        binary = work / 'interaction'
        subprocess.run([str(luce), 'build', str(ROOT / 'src/tests/interaction.luc'), '--native', '--opt', str(level), '-o', str(binary)], check=True, env=env, timeout=180)
        subprocess.run([str(binary)], check=True, env=env, timeout=30)
        clean()
    invalid = work / 'invalid.luc'
    invalid.write_text('pub func main(arguments: list[str]) -> int!:\n    return absent\n', encoding='utf-8', newline='\n')
    result = subprocess.run([str(luce), 'build', str(invalid), '-o', str(output / 'invalid')], capture_output=True, text=True, env=env, timeout=60)
    assert result.returncode != 0 and 'absent' in result.stderr, result
    assert sorted(p.name for p in output.iterdir()) == expected_outputs
    clean()
print('PASS native demo builds, application interactions and clean output')
