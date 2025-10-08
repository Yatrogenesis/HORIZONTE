import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from horizonte.mitg.iit_discrete import tpm_xor_chain
from horizonte.mitg.iit30 import phi_effect_iit30, index_to_bits


def test_iit30_effect_repertoire_valid():
    tp = tpm_xor_chain()
    n = 2
    # mechanism M = {0,1} with state [1,0], purview P={1}
    M = (0, 1)
    P = (1,)
    m_state = [1, 0]
    res = phi_effect_iit30(tp, n, M, P, m_state)
    # distribution sums to 1 and phi >= 0
    assert np.isclose(res.full.sum(), 1.0)
    assert res.phi >= 0.0

