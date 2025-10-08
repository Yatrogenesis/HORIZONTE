import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

import sys
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from horizonte.sch.cml import CML, CMLParams
from horizonte.mitg.topology import o_information_gaussian


def main():
    out_dir = ROOT / 'docs'
    out_dir.mkdir(parents=True, exist_ok=True)
    p = CMLParams(n=128, r=3.9, kappa=0.14, noise=0.001, seed=1)
    cml = CML(p)
    W = 60
    steps = 600
    series = []
    ovals = []
    for t in range(steps):
        series.append(cml.step().copy())
        if t >= W and t % 5 == 0:
            win = np.array(series[-W:])
            m = o_information_gaussian(win)
            ovals.append(float(m['Oinfo']))

    # Series mean plot
    means = [float(s.mean()) for s in series]
    plt.figure(figsize=(7, 2.2))
    plt.plot(means)
    plt.title('CML: mean activity over time')
    plt.tight_layout()
    plt.savefig(out_dir / 'example_series_plot.png', dpi=160)
    plt.close()

    # O-info evolution plot
    plt.figure(figsize=(7, 2.2))
    plt.plot(ovals)
    plt.title('O-information (Gaussian) over time')
    plt.tight_layout()
    plt.savefig(out_dir / 'example_phi_plot.png', dpi=160)
    plt.close()
    print('Wrote example plots to docs/')


if __name__ == '__main__':
    main()

