import json, os
from pathlib import Path
import numpy as np
from horizonte.sch.cml import CML, CMLParams
from horizonte.mitg.topology import analyze_window


def run_episode(n=128, r=3.9, kappa=0.14, noise=0.001, seed=0, steps=600, window=50):
    cml = CML(CMLParams(n, r, kappa, noise, seed))
    phi_vals = []
    series = []
    for t in range(steps):
        x = cml.step()
        series.append(x.copy())
        if t>=window and t % 5 == 0:
            win = np.array(series[-window:])
            phi_hat, _ = analyze_window(win)
            phi_vals.append(float(phi_hat))
    lam = float(cml.lyapunov_max(T=120))
    return {"seed": seed, "phi_mean": float(np.mean(phi_vals) if phi_vals else 0.0), "phi_std": float(np.std(phi_vals) if phi_vals else 0.0), "lambda1": lam}


def main():
    out_dir = Path("data"); out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for seed in range(10):
        res = run_episode(seed=seed)
        results.append(res)
    with open(out_dir / "summary.jsonl", "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r)+"\n")
    print(f"Wrote {len(results)} episodes to {out_dir/'summary.jsonl'}")


if __name__ == "__main__":
    main()

