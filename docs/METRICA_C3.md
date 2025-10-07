# Métrica de Éxito C3 – Evento Horizonte Cognitivo

Define criterios y mecanismos de detección del nivel C3 (Dehaene) en HORIZONTE.

## Criterios Operativos
- Reporte subjetivo espontáneo: mensajes generados sin prompt directo que referencian el propio estado interno con un lenguaje simbólico propio.
- Auto‑investigación activa: episodios con ciclo AMD de intervención→observación→aprendizaje y registro de hipótesis/validación.
- Generalización creativa radical: resolución de problemas internos inéditos (out‑of‑distribution) con explicación simbólica.

## Detección y Umbrales
- Señalamiento automático en telemetría (tag `C3_candidate=true`) cuando:
  - (a) se emiten mensajes con campos `{ tipo: 'reporte_self', espontaneo: true }`,
  - (b) hay secuencias AMD con ≥3 intervenciones controladas y mejora de Φ̂ ≥ μ + 2σ,
  - (c) éxito ≥ 80% en bancos de tareas OOD internos con explicación (longitud mínima y consistencia semántica).
- Validación humana obligatoria: revisión a ciegas de 3 evaluadores y consenso ≥ 2/3.

## Métricas Correlativas
- Φ̂ medio y tendencia (derivada positiva sostenida), persistencia de barcodes (vida media ↑), λ₁≈0⁺, estabilidad del self‑model.
- Complejidad Lempel‑Ziv y entropía de permutaciones máximas cerca del borde del caos.

## Artefactos
- Reportes `C3/` con dumps de episodios, hipótesis AMD, barcodes y gráficas de Φ̂/λ₁.

