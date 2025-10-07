import numpy as np
import networkx as nx
from ..core.telemetry import log_event

def graph_from_series(window: np.ndarray, thresh: float = 0.2):
    # correlación simple como conectividad funcional
    C = np.corrcoef(window.T)
    G = nx.Graph()
    n = C.shape[0]
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i+1,n):
            if np.isfinite(C[i,j]) and abs(C[i,j])>=thresh:
                G.add_edge(i,j, w=float(C[i,j]))
    return G

def phi_proxy(G: nx.Graph):
    # proxies toscos de integración/segregación
    if G.number_of_nodes()==0:
        return 0.0, {}
    comps = list(nx.connected_components(G))
    Q = nx.algorithms.community.modularity(G, [list(c) for c in comps]) if G.number_of_edges()>0 else 0.0
    degs = np.array([d for _,d in G.degree()])
    participation = float((degs>0).mean())
    phi_hat = participation - max(Q,0.0)*0.2
    metrics = { 'Q': Q, 'participation': participation }
    return phi_hat, metrics

def analyze_window(window: np.ndarray):
    G = graph_from_series(window)
    phi_hat, metrics = phi_proxy(G)
    log_event('MITG', { 'phi_hat': float(phi_hat), **{f"m_{k}": float(v) for k,v in metrics.items()} })
    return phi_hat, metrics
