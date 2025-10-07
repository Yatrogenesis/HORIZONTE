import numpy as np
from dataclasses import dataclass
from ..core.telemetry import log_event

@dataclass
class AMDState:
    K: np.ndarray | None = None

class AMD:
    def __init__(self):
        self.state = AMDState()

    @staticmethod
    def features(z: np.ndarray):
        # diccionario simple: [z, z^2]
        return np.concatenate([z, z**2], axis=-1)

    def fit_edmd(self, Z: np.ndarray):
        # Z shape: (T, F) with T>=2; build shifted pairs
        if Z.ndim != 2 or Z.shape[0] < 2:
            raise ValueError("EDMD requires Z with shape (T>=2, F)")
        Phi = self.features(Z[:-1])
        Phi_next = self.features(Z[1:])
        G = Phi.T @ Phi + 1e-6*np.eye(Phi.shape[1])
        A = Phi.T @ Phi_next
        K = np.linalg.lstsq(G, A, rcond=None)[0]
        self.state.K = K
        rs = max(abs(np.linalg.eigvals(K)))
        log_event('AMD', { 'rho_K': float(rs) })
        return K, rs

    def control_signal(self, rho_K: float, target=(0.0, 1.05)):
        low, high = target
        # política simple: apunta a radio espectral cercano pero < high
        if rho_K>high: return { 'dkappa': +0.02, 'dsigma': +0.01, 'dg': -0.01 }
        if rho_K<1.0: return { 'dkappa': -0.01, 'dsigma': -0.005, 'dg': +0.01 }
        return { 'dkappa': 0.0, 'dsigma': 0.0, 'dg': 0.0 }
