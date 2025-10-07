import os, sys
from pathlib import Path

# Ensure src is on path when running locally without install
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from horizonte.core.config import SimConfig
from horizonte.cli import run_episode


def test_run_episode_smoke():
    # Reduce pasos para test rápido
    cfg = SimConfig(n=64, steps=60, window=20, kappa=0.12, noise=0.001)
    run_episode(cfg)
    # Comprueba que se generó al menos un log
    assert os.path.isdir('logs')
