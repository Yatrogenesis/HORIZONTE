import numpy as np
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from horizonte.mitg.topology import o_information_gaussian
from horizonte.mitg.oinfo import o_information_knn


def test_oinfo_gaussian_vs_knn_sign():
    rng = np.random.default_rng(0)
    T = 600
    # Create Gaussian with small synergy (positive O) by correlated triplet
    X1 = rng.normal(size=T)
    X2 = X1 + 0.1 * rng.normal(size=T)
    X3 = X1 + X2 + 0.1 * rng.normal(size=T)
    W = np.stack([X1, X2, X3], axis=1)
    mg = o_information_gaussian(W)
    Og = mg['Oinfo']
    Ok, _ = o_information_knn(W, k=5)
    # Expect same sign
    assert np.sign(Og) == np.sign(Ok) or np.isclose(Ok, 0.0, atol=1e-1)
