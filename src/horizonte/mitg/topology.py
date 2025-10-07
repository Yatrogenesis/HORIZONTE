import numpy as np
import networkx as nx
from ..core.telemetry import log_event


def _regularized_cov(X: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    # X shape (T, N): samples over time of N variables
    Xc = X - X.mean(axis=0, keepdims=True)
    S = (Xc.T @ Xc) / max(1, (Xc.shape[0] - 1))
    # regularize to ensure PD
    S = S + eps * np.eye(S.shape[0])
    return S


def _gaussian_entropy_from_cov(S: np.ndarray) -> float:
    # differential entropy H(X) for multivariate Gaussian with covariance S
    n = S.shape[0]
    sign, logdet = np.linalg.slogdet(S)
    if sign <= 0:
        # further regularize if needed
        evals, evecs = np.linalg.eigh(S)
        evals = np.clip(evals, 1e-12, None)
        S = (evecs * evals) @ evecs.T
        sign, logdet = np.linalg.slogdet(S)
    return 0.5 * (n * (1.0 + np.log(2 * np.pi)) + logdet)


def _gaussian_conditional_variance(S: np.ndarray, i: int) -> float:
    # variance of X_i | X_{-i} for Gaussian with covariance S
    idx = np.arange(S.shape[0])
    mask = idx != i
    S_ii = S[i, i]
    S_iR = S[i, mask]
    S_RR = S[np.ix_(mask, mask)]
    # solve for conditional variance: S_ii - S_iR S_RR^{-1} S_Ri
    try:
        inv_RR = np.linalg.inv(S_RR)
    except np.linalg.LinAlgError:
        inv_RR = np.linalg.pinv(S_RR)
    cond_var = float(S_ii - S_iR @ inv_RR @ S_iR.T)
    return max(cond_var, 1e-12)


def total_correlation_gaussian(window: np.ndarray) -> float:
    S = _regularized_cov(window)
    H = _gaussian_entropy_from_cov(S)
    H_sum = 0.0
    for i in range(S.shape[0]):
        H_sum += 0.5 * (1.0 + np.log(2 * np.pi)) + 0.5 * np.log(S[i, i])
    return float(H_sum - H)


def dual_total_correlation_gaussian(window: np.ndarray) -> float:
    S = _regularized_cov(window)
    H = _gaussian_entropy_from_cov(S)
    cond_sum = 0.0
    for i in range(S.shape[0]):
        var_i = _gaussian_conditional_variance(S, i)
        cond_sum += 0.5 * (1.0 + np.log(2 * np.pi)) + 0.5 * np.log(var_i)
    return float(H - cond_sum)


def o_information_gaussian(window: np.ndarray) -> dict:
    tc = total_correlation_gaussian(window)
    dtc = dual_total_correlation_gaussian(window)
    return { 'TC': tc, 'DTC': dtc, 'Oinfo': float(dtc - tc) }


def graph_from_series(window: np.ndarray, thresh: float = 0.2):
    # correlación como conectividad funcional (para análisis estructural, no como métrica de Φ)
    C = np.corrcoef(window.T)
    G = nx.Graph()
    n = C.shape[0]
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if np.isfinite(C[i, j]) and abs(C[i, j]) >= thresh:
                G.add_edge(i, j, w=float(C[i, j]))
    return G


def analyze_window(window: np.ndarray):
    metrics = o_information_gaussian(window)
    # Opcional: métricas de grafo estructurales
    try:
        G = graph_from_series(window)
        comps = list(nx.connected_components(G))
        Q = (
            nx.algorithms.community.modularity(G, [list(c) for c in comps])
            if G.number_of_edges() > 0
            else 0.0
        )
        metrics.update({ 'Q': float(Q), 'edges': G.number_of_edges() })
    except Exception:
        pass
    log_event('MITG', { **{ f'm_{k}': float(v) for k, v in metrics.items() if isinstance(v,(int,float)) } })
    # Devolvemos O-information como señal principal
    return float(metrics['Oinfo']), metrics
