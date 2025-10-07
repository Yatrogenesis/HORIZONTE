import numpy as np
from dataclasses import dataclass
from ..core.telemetry import log_event

@dataclass
class CMLParams:
    n:int
    r:float
    kappa:float
    noise:float
    seed:int

class CML:
    def __init__(self, p: CMLParams):
        self.p = p
        self.rng = np.random.default_rng(p.seed)
        self.x = self.rng.random(p.n)
        # anillo
        self.nei = lambda v: np.roll(v,1) + np.roll(v,-1)

    @staticmethod
    def f(x, r):
        return r*x*(1-x)

    def step(self):
        x = self.x
        fx = self.f(x, self.p.r)
        neigh = 0.5*(self.f(np.roll(x,1), self.p.r) + self.f(np.roll(x,-1), self.p.r))
        x_next = (1-self.p.kappa)*fx + self.p.kappa*neigh
        if self.p.noise>0:
            x_next += self.p.noise*self.rng.standard_normal(x.shape)
        self.x = np.clip(x_next, 0.0, 1.0)
        return self.x

    def lyapunov_max(self, T=200):
        # estimación sencilla del exponente de Lyapunov máximo
        eps = 1e-7
        v = self.rng.standard_normal(self.p.n)
        v /= np.linalg.norm(v)+1e-12
        s=0.0
        for _ in range(T):
            # Jacobiano aproximado diagonal + acoplamiento lineal
            J = self.p.r*(1-2*self.x)
            v = (1-self.p.kappa)*J*v + 0.5*self.p.kappa*(np.roll(J*v,1)+np.roll(J*v,-1))
            nv = np.linalg.norm(v)+1e-12
            s += np.log(nv+eps)
            v /= nv
            self.step()
        return s/T

    def run(self, steps:int, log_every:int=10):
        series = []
        for t in range(steps):
            x = self.step()
            if t % log_every == 0:
                log_event('SCH', { 't': t, 'mean': float(x.mean()), 'std': float(x.std()) })
            series.append(x.copy())
        return np.array(series)
