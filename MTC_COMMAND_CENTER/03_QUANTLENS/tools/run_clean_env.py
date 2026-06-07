"""
Launch strat_batch_remaining.py with a CLEAN Windows environment (no MSYS2 vars/paths).

D009 root cause: MSYS2 env vars (MSYSTEM=MINGW64) AND MSYS2 PATH entries are inherited
by all child processes launched from Claude Code's bash/PowerShell tools. MSYS2's bin
directories are prepended to PATH, causing scipy DLL loading to find MSYS2-built
libopenblas/libgfortran DLLs instead of the Windows scipy build → hang.

Fix: strip MSYS2 env vars and MSYS2 PATH entries before launching the sweep.

Usage (from bash, in tools/ dir):
  MEGA_WORKERS=8 MEGA_OUTPUT_DIR=/path/to/run_dir python run_clean_env.py [--strategy ...]

This script itself doesn't import scipy so it's safe to call from bash.
"""
from __future__ import annotations
import os
import subprocess
import sys

# MSYS2-specific env vars to remove
MSYS2_VARS = {
    'MSYSTEM', 'MSYS2_PATH_TYPE', 'CYGWIN', 'MANPATH', 'INFOPATH',
    'PKG_CONFIG_PATH', 'ACLOCAL_PATH', 'ORIGINAL_PATH', 'MSYS_HOME',
    'MINGW_PREFIX', 'MINGW_CHOST', 'MINGW_PACKAGE_PREFIX',
    'TERM',  # cygwin terminal type
}

# MSYS2 PATH directory markers
MSYS2_PATH_MARKERS = (
    'msys64', 'msys2', 'mingw64', 'mingw32', 'usr/bin', 'usr/local/bin',
    r'\mingw64\bin', r'\usr\bin', r'/mingw64/bin', r'/usr/bin',
)

def clean_path(path_str: str) -> str:
    parts = path_str.split(os.pathsep)
    clean = []
    for p in parts:
        p_lower = p.lower().replace('/', '\\')
        if any(m.lower() in p_lower for m in MSYS2_PATH_MARKERS):
            continue
        clean.append(p)
    return os.pathsep.join(clean)

clean_env = {}
for k, v in os.environ.items():
    if k in MSYS2_VARS:
        continue
    if k == 'PATH':
        clean_env[k] = clean_path(v)
    else:
        clean_env[k] = v

# Force single-threaded BLAS (prevents OpenBLAS multi-thread deadlock on Windows)
clean_env['OMP_NUM_THREADS'] = '1'
clean_env['MKL_NUM_THREADS'] = '1'
clean_env['OPENBLAS_NUM_THREADS'] = '1'
clean_env['NUMEXPR_NUM_THREADS'] = '1'
clean_env['NUMBA_NUM_THREADS'] = '1'

# Preserve MEGA env vars from parent
for key in ('MEGA_WORKERS', 'MEGA_OUTPUT_DIR', 'MEGA_HEARTBEAT_PATH'):
    if key in os.environ:
        clean_env[key] = os.environ[key]

script_dir = os.path.dirname(os.path.abspath(__file__))
cmd = [sys.executable, os.path.join(script_dir, 'strat_batch_remaining.py')] + sys.argv[1:]

removed = MSYS2_VARS & set(os.environ)
print(f"[run_clean_env] removed MSYS2 vars: {removed}", flush=True)
original_path_count = len(os.environ.get('PATH', '').split(os.pathsep))
clean_path_count = len(clean_env.get('PATH', '').split(os.pathsep))
print(f"[run_clean_env] PATH: {original_path_count} → {clean_path_count} entries (stripped MSYS2)", flush=True)
print(f"[run_clean_env] launching: python strat_batch_remaining.py {' '.join(sys.argv[1:])}", flush=True)

result = subprocess.run(cmd, env=clean_env, cwd=script_dir)
sys.exit(result.returncode)
