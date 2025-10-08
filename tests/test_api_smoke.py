import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import numpy as np
import pytest

try:
    from fastapi.testclient import TestClient  # type: ignore
    from horizonte.api.server import app
except Exception:
    app = None


@pytest.mark.skipif(app is None, reason="fastapi not installed")
def test_api_endpoints_smoke():
    client = TestClient(app)
    # O-info endpoint
    W = np.random.randn(80, 3).tolist()
    r = client.post('/metrics/oinfo', json={"window": W, "knn_k": 3})
    assert r.status_code == 200
    data = r.json()
    assert 'gaussian' in data and 'knn' in data
    # phi_si endpoint with identity TPM (2 bits)
    tp = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    r2 = client.post('/iit/phi_si', json={"tpm": tp})
    assert r2.status_code == 200
    assert abs(r2.json()["phi_si"]) < 1e-9

