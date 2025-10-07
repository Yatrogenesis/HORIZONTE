import numpy as np
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from horizonte.mitg.iit_discrete import (
    phi_stochastic_interaction,
    stationary_uniform,
    tpm_identity,
    tpm_xor_chain,
)


def test_phi_si_identity_zero():
    tp = tpm_identity(2)
    p = stationary_uniform(2)
    phi, P = phi_stochastic_interaction(tp, p)
    assert np.isclose(phi, 0.0, atol=1e-9)


def test_phi_si_xor_positive():
    tp = tpm_xor_chain()
    p = stationary_uniform(2)
    phi, P = phi_stochastic_interaction(tp, p)
    assert phi > 0.0
