import numpy as np
import argparse
from collections import deque
from .core.config import SimConfig
from .sch.cml import CML, CMLParams
from .mitg.topology import analyze_window
from .amd.koopman import AMD
from .eca.agents import ECASwarm
from .icgq.qaoa import suggest_rewire
from .core.telemetry import log_event

def run_episode(cfg: SimConfig = SimConfig()):
    cml = CML(CMLParams(cfg.n, cfg.r, cfg.kappa, cfg.noise, cfg.seed))
    amd = AMD()
    eca = ECASwarm(n=max(8, cfg.n//32), seed=cfg.seed)
    series = []
    phi_vals = []
    # buffer temporal para EDMD con al menos 2 observaciones
    Zg_buf: deque = deque(maxlen=10)
    for t in range(cfg.steps):
        x = cml.step()
        series.append(x.copy())
        if t>=cfg.window and t % 10 == 0:
            win = np.array(series[-cfg.window:])  # (W, N)
            phi_hat, _ = analyze_window(win)
            phi_vals.append(phi_hat)
            # construir punto de estado global (media y std de phi reciente)
            if len(phi_vals)>=1:
                Zg_point = np.array([np.mean(phi_vals[-5:]) if len(phi_vals)>=5 else phi_hat,
                                     np.std(phi_vals[-5:]) if len(phi_vals)>=5 else 0.0], dtype=float)
                Zg_buf.append(Zg_point)
            if len(Zg_buf) >= 2:
                Zg = np.vstack(Zg_buf)
                K, rho = amd.fit_edmd(Zg)
                ctrl = amd.control_signal(rho)
                eco = eca.propose()
                # aplicar control agregado (limitado)
                cml.p.kappa = float(np.clip(cml.p.kappa + 0.5*(ctrl['dkappa']) , 0.0, 0.5))
                cml.p.noise = float(np.clip(cml.p.noise + 0.5*(ctrl['dsigma']), 0.0, 0.1))
                # eco dg afecta un "g" efectivo: aquí lo modelamos como ajuste pequeño en r
                cml.p.r = float(np.clip(cml.p.r + 0.1*eco['dg'], 3.5, 3.99))
                trend = (phi_vals[-1]-phi_vals[-5]) if len(phi_vals)>5 else 0.0
                suggest_rewire(trend)
                log_event('CTRL', { 't': t, 'kappa': cml.p.kappa, 'noise': cml.p.noise, 'r': cml.p.r, 'phi': phi_hat })
    # reporte final
    lam = cml.lyapunov_max(T=100)
    log_event('REPORT', { 'lambda1': float(lam), 'phi_mean': float(np.mean(phi_vals) if phi_vals else 0.0) })


def main():
    ap = argparse.ArgumentParser(description='HORIZONTE simulation episode')
    ap.add_argument('--n', type=int, default=SimConfig.n, help='nodos del CML')
    ap.add_argument('--r', type=float, default=SimConfig.r, help='parametro mapa logistico')
    ap.add_argument('--kappa', type=float, default=SimConfig.kappa, help='acoplamiento')
    ap.add_argument('--noise', type=float, default=SimConfig.noise, help='ruido')
    ap.add_argument('--steps', type=int, default=SimConfig.steps, help='pasos simulacion')
    ap.add_argument('--seed', type=int, default=SimConfig.seed, help='semilla')
    ap.add_argument('--window', type=int, default=SimConfig.window, help='ventana analisis')
    args = ap.parse_args()
    cfg = SimConfig(n=args.n, r=args.r, kappa=args.kappa, noise=args.noise, steps=args.steps, seed=args.seed, window=args.window)
    run_episode(cfg)

if __name__ == '__main__':
    main()
