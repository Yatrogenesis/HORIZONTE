from ..core.telemetry import log_event

def suggest_rewire(phi_trend: float):
    # heurística mínima: si la tendencia de Φ^ es plana/negativa, sugerir sparsificar levemente
    dw = -0.01 if phi_trend<=0 else 0.0
    log_event('ICGQ', { 'rewire_suggestion': dw })
    return { 'dA_sparsify': dw }
