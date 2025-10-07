import numpy as np
from dataclasses import dataclass
from ..core.telemetry import log_event

@dataclass
class Agent:
    w: float = 0.0  # peso de influencia

class ECASwarm:
    def __init__(self, n:int, seed:int=0):
        self.rng = np.random.default_rng(seed)
        self.agents = [Agent(w=float(self.rng.uniform(-0.01,0.01))) for _ in range(n)]

    def propose(self):
        # propuesta agregada de micro-reconfiguración
        delta = sum(a.w for a in self.agents)
        log_event('ECA', { 'delta_proposal': float(delta) })
        return { 'dkappa': 0.0, 'dsigma': 0.0, 'dg': delta }
