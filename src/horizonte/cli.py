import numpy as np
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
    for t in range(cfg.steps):
        x = cml.step()
        series.append(x.copy())
        if t>=cfg.window and t % 10 == 0:
            win = np.array(series[-cfg.window:])  # (W, N)
            # resumen simple (F): media y var por nodo
            Z = np.stack([win.mean(0), win.var(0)], axis=-1).reshape(win.shape[1], -1)
            phi_hat, _ = analyze_window(win)
            phi_vals.append(phi_hat)
            if len(phi_vals)>5:
                Zg = np.array([[np.mean(phi_vals[-5:]), np.std(phi_vals[-5:])]])
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
    run_episode()

if __name__ == '__main__':
    main()
