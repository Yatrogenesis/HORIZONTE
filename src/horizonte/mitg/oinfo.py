from __future__ import annotations

import math
from typing import Tuple

import numpy as np
from scipy.special import digamma, gamma
from sklearn.neighbors import NearestNeighbors


def _unit_ball_volume(d: int) -> float:
    return (math.pi ** (d / 2.0)) / gamma(d / 2.0 + 1.0)


def entropy_knn(X: np.ndarray, k: int = 3) -> float:
    """Kozachenko–Leonenko k-NN differential entropy estimator.

    Args:
        X: array (n_samples, n_dims)
        k: number of neighbors
    Returns:
        Estimated differential entropy in nats.
    """
    X = np.asarray(X, dtype=float)
    n, d = X.shape
    if n <= k:
        raise ValueError("Need n > k for kNN entropy")
    # k-NN distances (exclude the point itself)
    nbrs = NearestNeighbors(n_neighbors=k + 1, algorithm="auto").fit(X)
    distances, _ = nbrs.kneighbors(X)
    # The k-th neighbor distance per sample (exclude self at idx 0)
    eps = distances[:, -1]
    c_d = _unit_ball_volume(d)
    return float(
        digamma(n) - digamma(k) + d * np.mean(np.log(eps + 1e-12)) + np.log(c_d) + d * np.log(2.0)
    )


def o_information_knn(window: np.ndarray, k: int = 3) -> Tuple[float, dict]:
    """O-information via kNN entropy estimator (non-Gaussian exact formulation with consistent estimator).

    O = DTC - TC,
    where TC = sum_i H(X_i) - H(X), and DTC = N*H(X) - sum_i H(X_{-i}).
    """
    X = np.asarray(window, dtype=float)
    if X.ndim != 2:
        raise ValueError("window must be 2D (T, N)")
    T, N = X.shape
    # entropies
    H_joint = entropy_knn(X, k=k)
    H_marg = [entropy_knn(X[:, [i]], k=k) for i in range(N)]
    # entropies of complements
    H_minus = [entropy_knn(np.delete(X, i, axis=1), k=k) for i in range(N)]
    TC = float(sum(H_marg) - H_joint)
    DTC = float(N * H_joint - sum(H_minus))
    O = float(DTC - TC)
    return O, {"TC": TC, "DTC": DTC, "H": H_joint}

