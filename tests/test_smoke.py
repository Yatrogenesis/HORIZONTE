import os
from horizonte.core.config import SimConfig
from horizonte.cli import run_episode


def test_run_episode_smoke():
    # Reduce pasos para test rápido
    cfg = SimConfig(n=64, steps=60, window=20, kappa=0.12, noise=0.001)
    run_episode(cfg)
    # Comprueba que se generó al menos un log
    assert os.path.isdir('logs')

