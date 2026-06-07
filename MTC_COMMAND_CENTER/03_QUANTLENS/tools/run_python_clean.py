"""
Run any Python script with clean env + scipy.stats shim (D009 fix).

Usage: python run_python_clean.py script.py [args...]

Strips MSYS2/Cygwin env vars and PATH entries, sets BLAS threads=1,
and auto-injects _scipy_shim to prevent scipy.stats import hang
(OpenBLAS 0.3.30 + Python 3.14 + DYNAMIC_ARCH deadlock on this hardware).

This wrapper itself doesn't import scipy, so it's safe to run from bash/tools.
"""
from __future__ import annotations
import os
import subprocess
import sys

MSYS2_VARS = {
    'MSYSTEM', 'MSYS2_PATH_TYPE', 'CYGWIN', 'MANPATH', 'INFOPATH',
    'PKG_CONFIG_PATH', 'ACLOCAL_PATH', 'ORIGINAL_PATH', 'MSYS_HOME',
    'MINGW_PREFIX', 'MINGW_CHOST', 'MINGW_PACKAGE_PREFIX',
}

MSYS2_PATH_MARKERS = ('msys', 'mingw', '/usr/bin', '/usr/local/bin', r'\usr\bin', r'\usr\local\bin')


def clean_path(path_str: str) -> str:
    parts = path_str.split(os.pathsep)
    return os.pathsep.join(
        p for p in parts
        if not any(m in p.lower().replace('/', os.sep) for m in MSYS2_PATH_MARKERS)
    )


clean_env = {}
for k, v in os.environ.items():
    if k in MSYS2_VARS:
        continue
    clean_env[k] = clean_path(v) if k == 'PATH' else v

for var in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    clean_env[var] = '1'

if len(sys.argv) < 2:
    print("Usage: python run_python_clean.py script.py [args...]", file=sys.stderr)
    print("       python run_python_clean.py -c code [args...]", file=sys.stderr)
    sys.exit(1)

script_dir = os.path.dirname(os.path.abspath(__file__))
SHIM_PREFIX = f'import sys; sys.path.insert(0, {script_dir!r}); import _scipy_shim; '

if sys.argv[1] == '-c':
    code = sys.argv[2]
    extra_args = sys.argv[3:]
    cmd = [sys.executable, '-c', SHIM_PREFIX + code] + extra_args
else:
    target = os.path.join(script_dir, sys.argv[1]) if not os.path.isabs(sys.argv[1]) else sys.argv[1]
    target_args = sys.argv[2:]
    inject = (
        f'{SHIM_PREFIX}'
        f'__file__ = {target!r}; '
        f'sys.argv = [{target!r}] + {target_args!r}; '
        f'exec(compile(open({target!r}).read(), {target!r}, "exec"))'
    )
    cmd = [sys.executable, '-c', inject]

result = subprocess.run(cmd, env=clean_env, cwd=script_dir)
sys.exit(result.returncode)
