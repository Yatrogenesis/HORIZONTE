import numpy as np
from ..core.telemetry import log_event


def persistent_homology(window: np.ndarray):
    """Compute simple PH summary from a time window (W, N) as point cloud in R^N.
    Tries ripser, then gudhi. Returns dict with summaries or None if unavailable.
    """
    X = np.asarray(window, dtype=float)
    try:
        from ripser import ripser
        res = ripser(X, maxdim=1)
        dgms = res.get('dgms', [])
        def total_persistence(diag):
            return float(np.sum((diag[:, 1] - diag[:, 0])[np.isfinite(diag).all(axis=1)])) if len(diag) else 0.0
        h0 = dgms[0] if len(dgms) > 0 else []
        h1 = dgms[1] if len(dgms) > 1 else []
        return { 'source': 'ripser', 'tp_h0': total_persistence(np.array(h0)), 'tp_h1': total_persistence(np.array(h1)) }
    except Exception:
        pass
    try:
        import gudhi as gd  # type: ignore
        rc = gd.RipsComplex(points=X, max_edge_length=10.0)
        st = rc.create_simplex_tree(max_dimension=2)
        st.persistence()
        # total persistence for H0, H1
        tp0 = tp1 = 0.0
        for dim, (b, d) in st.persistence_intervals_in_dimension(0):
            if np.isfinite(b) and np.isfinite(d): tp0 += (d - b)
        for dim, (b, d) in st.persistence_intervals_in_dimension(1):
            if np.isfinite(b) and np.isfinite(d): tp1 += (d - b)
        return { 'source': 'gudhi', 'tp_h0': float(tp0), 'tp_h1': float(tp1) }
    except Exception:
        log_event('MITG', { 'tda': 'unavailable' })
        return None


def topo_proxy_phi(window: np.ndarray):
    """Topological proxy for integration: normalized total persistence in H1.
    Returns (phi_topo, details) where phi_topo in [0, 1] (heuristic normalization).
    """
    res = persistent_homology(window)
    if not res:
        return 0.0, { 'tda': 'unavailable' }
    tp_h1 = res.get('tp_h1', 0.0)
    # heuristic: map total persistence to (0,1) via 1 - exp(-tp)
    phi_topo = float(1.0 - np.exp(-tp_h1))
    details = { 'source': res.get('source', 'unknown'), 'tp_h0': res.get('tp_h0', 0.0), 'tp_h1': tp_h1 }
    log_event('MITG', { 'phi_topo': phi_topo, **details })
    return phi_topo, details

