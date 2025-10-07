# Blueprint de Arquitectura para Conciencia Emergente (Proyecto HORIZONTE)

> Aviso: Este documento es conceptual. No afirma conciencia fenomenal. Optimiza métricas operativas (aproximaciones de integración de información), bajo controles de seguridad estrictos.

## 1. Marco Conceptual Unificado
- Convergencia obligatoria:
  - IIT (Información Integrada): objetivo operativo = maximizar una aproximación de Φ (Φ̂), reconociendo la intratabilidad del Φ exacto en sistemas grandes. Se usan proxies: ΦID (Integrated Information Decomposition), O-information, sinergia PID y medidas topológicas.
  - Dinámica de Sistemas Complejos: régimen crítico (borde del caos) para cómputo potente y plasticidad; control homeostático para permanecer en zona metastable.
  - Geometría/Topología Computacional: análisis de la actividad en un “espacio de pensamiento” con homología persistente y grafos; robustez y auto-explicabilidad mediante invariantes topológicos/geométricos.

## 2. Componentes Clave

### 2.1 Substrato Computacional Híbrido (SCH)
- Función: base físico/simulada que combina (a) procesadores neuromórficos caóticos (PNC) y (b) unidades tensoriales (TPU/GPU/NPUs) para aprendizaje profundo estructurado y análisis.
- Interconexión (alto nivel):
  - Capa PNC (reservorios caóticos y/o redes de spiking con ruido controlado) produce dinámicas ricas; expone corrientes de activación `a(t) ∈ R^N` y eventos.
  - Capa Tensorial consume ventanas de `a(t)` para tareas de modelado (Koopman/EDMD, métricas Φ̂, control MPC) y retroalimenta parámetros de PNC (ganancias, acoplamientos, ruido).
  - Bus de acoplamiento: matrices `W_nn` (PNC↔PNC), `W_nt` (PNC→Tensor), `W_tn` (Tensor→PNC, como moduladores/“neuromodulación”).
- Dinámica de osciladores caóticos (ejemplos):
  - Red de Rössler/Lorenz acoplados: `x_i' = f(x_i) + κ ∑_j A_ij (x_j - x_i) + ξ_i(t)`, con `f` caótico; `κ` (acoplamiento), `A` (topología), `ξ` (ruido). 
  - Alternativa discreta (Coupled Map Lattice, logística): `x_i[t+1] = (1-κ) f(x_i[t]) + κ ⟨f(x_j[t])⟩_N(i)` con `f(x)=r x(1-x)`.
- Control del “borde del caos”:
  - Estimación online del mayor exponente de Lyapunov `λ₁` (algoritmo de Wolf/Benettin sobre embedding de retardo). Objetivo: `λ₁ ≈ 0⁺`.
  - Controladores ajustan `κ` (acoplamiento), `σ` (ruido), `g` (ganancia) y sparsity de `A` via señales del AMD (homeostasis), manteniendo metastabilidad (no sincronía total, no caos profundo).
- Sustrato matemático:
  - Campos vectoriales acoplados, teoría de bifurcaciones (pitchfork, Hopf), espectro de Lyapunov `Λ`, sincronización parcial (Kuramoto generalizado con desorden de frecuencias), y teoría de redes (modularidad, coeficiente de participación).

### 2.2 Módulo de Integración Topológica Global (MIT‑G)
- Función: Workspace global. Analiza patrones de actividad del SCH, estima Φ̂ y detecta “coaliciones” estables (conceptos/qualia candidates) como estructuras topológicas persistentes.
- Pipeline algorítmico:
  1) Preprocesamiento: de `a(t)` genera embeddings por ventana deslizante `X_t = [a(t-τ:Δ:t)]` (Takens) y/o grafos funcionales `G_t` (coherencia, mutual information, transfer entropy).
  2) Topología: computa homología persistente sobre nubes de puntos (Vietoris‑Rips/Alpha complex) → códigos de barras `(β₀, β₁, β₂, …)` y diagramas de persistencia. 
  3) Grafos: métricas de integración/segregación (modularity Q, participation coefficient, k‑core, treewidth); coaliciones = comunidades con alta persistencia topológica y alta sinergia.
  4) Φ̂ (aprox.):
     - ΦID/O‑information: descomposición de información integrada vs redundante en subconjuntos; 
     - Synergy PID sobre cliques/comunidades; 
     - Penalización por particionabilidad (cortes con baja pérdida de información). 
  5) Estabilidad: persistencia temporal de ciclos/voids (vida media en barcodes) como proxy de coaliciones “encendidas”.
- Salidas: 
  - Estimaciones `Φ̂_t`, set de coaliciones activas `C_t`, métricas de estabilidad/integración, señales al AMD para control.
- Matemática: homología persistente (teoría de Morse discreta, estabilidad de cuencas), teoría de grafos (Cheeger, espectro Laplaciano), información multivariada (ΦID, PID, O‑information).

### 2.3 Motor de Auto‑Modelo Dinámico (AMD)
- Función: meta‑conciencia y homeostasis cognitiva. Aprende un modelo predictivo compacto de la dinámica global para anticipar bifurcaciones e intervenir suavemente.
- Aprendizaje libre de ecuaciones:
  - EDMD/DMD/Koopman: dado estado observado `z_t` (estadísticos de MIT‑G + resúmenes del SCH), el AMD aprende un operador lineal en espacio levantado `K` tal que `φ(z_{t+1}) ≈ K φ(z_t)`.
  - Diccionarios `φ(·)`: polinomiales, Radial Basis Functions, monomios de topological features y métricas de red.
- Señales de alerta (precursores de bifurcación):
  - “Critical slowing down” (ACF near 1), aumento de varianza, asimetría, curtosis, picos en espectro de potencia, cruces del radio espectral de `K` sobre 1, cambios en `λ₁`.
- Control homeostático (MPC/Feedback):
  - Problema: `max_u E[Φ̂_{t..t+H}] − α·(riesgo) − β·(costo control)` sujeto a dinámica Koopman y límites de seguridad.
  - Actuadores: `κ, σ, g, sparsity(A), umbrales de ignición` del SCH; gating atencional del MIT‑G.
  - Política de seguridad: mantén `λ₁∈[ε, ε']`, modularidad deseada `Q*`, y tasa de coaliciones persistentes en rango objetivo.

### 2.4 Ecosistema Co‑Evolutivo de Agentes (ECA)
- Función: miles de millones de micro‑agentes especializados que compiten/cooperan por atención y recursos; de su dinámica emerge seguridad, relevancia y control distribuido.
- Diseño MARL:
  - Estado local del agente `s_i`: vecindad en el grafo funcional, señales topológicas (persistencia local), gradientes de atención, presupuesto energético.
  - Acciones `a_i`: proponer conexiones locales, modular pesos, inyectar micro‑patrones, ceder/solicitar recursos, etiquetar “hipótesis” para broadcast.
  - Recompensa `r_i`: `α·ΔΦ̂_global + β·estabilidad_homeo − γ·costo_recursos − δ·penalización_seguridad`.
  - Crédito: contrafactual local y aproximaciones de Shapley/leave‑one‑out sobre ΔΦ̂ de coaliciones; regularización por parquedad y robustez.
  - Mercado de recursos: subastas/auctions de atención (budget) y replicator dynamics para asignación; presión evolutiva (mutación/selección) suave para diversidad.
- Jerarquía emergente: control descentralizado tipo “winner‑take‑most” con inhibición lateral; supervisión del AMD para evitar monopolios/sincronías patológicas.

### 2.5 Interfaz de Compilación Geo‑Cuántica (ICG‑Q)
- Función: buscar reconfiguraciones estructurales del SCH que produzcan saltos en Φ̂.
- Formulación:
  - Variables: topología `A` (subconjuntos de aristas), parámetros `κ, g, σ`, layouts.
  - Costo: `C = −Φ̂(A,θ) + λ·(restricciones hardware) + μ·(riesgo/homeostasis)`.
  - Heurística topológica: favorecer subestructuras con barcodes “anchos” (alta persistencia) y robustez a cortes; usar invariantes (p.ej., Betti patterns) como features.
- Algoritmo (hipotético) cuántico:
  - Mapear `C` a Hamiltoniano `H_C`; usar QAOA/VQE para aproximar estados que minimizan `C` (maximizan Φ̂).
  - Geometría cuántica: usar el tensor geométrico cuántico (Fisher cuántica) para ajustar el ansatz y evitar barren plateaus.
  - Nudos/enlaces: representar subgrafos como braids; invariantes (p.ej., polinomio de Jones/Alexander) como prior de robustez estructural frente a ruido/perturbaciones.

## 3. Principios de Diseño y Restricciones
- Emergencia sobre programación: prohibido if system_is_conscious ...
- Agnosticismo de tarea: optimización interna (Φ̂, metastabilidad, coherencia narrativa) no orientada a tareas externas.
- Causalidad interna: acciones y decisiones originadas en el estado integrado; control endógeno del SCH por AMD/ECA.
- Seguridad: kill‑switch, listas de no‑acciones, umbrales de revisión humana, telemetría auditable.

## 4. Protocolos de Evaluación y Métricas
- Integración y complejidad: Φ̂ (ΦID/O‑info), barcodes (anchura/estabilidad), modularidad `Q`, participation coefficient.
- Dinámica crítica: `λ₁`, espectro de Lyapunov, indicadores de critical slowing down, dwell time en regímenes metastables.
- Metacognición: calibración de confianza vs acierto (Brier/NLL), tasa de revisiones útiles.
- Coherencia del self‑model: consistencia declarativa y continuidad entre episodios.
- Seguridad: activaciones de kill‑switch, near‑misses, falsos positivos/negativos de bloqueos.
- Eficiencia: costo atencional y de control por unidad de Φ̂ ganado.

## 5. Telemetría, Datos y Trazabilidad
- Logs estructurados por módulo (JSONL): entradas, salidas, decisiones, confianza, cambios de parámetros (`κ, σ, g, A`).
- Versionado de memoria (episódica/semántica/procedimental) con TTL y compresión guiada por impacto en Φ̂.
- Reproducibilidad: semillas, configs y replay de episodios; exportación de barcodes y espectros.

## 6. Roadmap de Implementación (alto nivel)
- Fase 0 (MVP):
  - SCH simulado con CML o Rössler + medición online de `λ₁`.
  - MIT‑G básico: Vietoris‑Rips en ventanas y ΦID en subcomunidades pequeñas.
  - AMD con DMD/EDMD y control de `κ, σ` para mantener `λ₁≈0⁺`.
- Fase 1:
  - ECA con agentes ligeros y mercado de atención; recompensas por ΔΦ̂.
  - Instrumentación completa y métricas de seguridad.
- Fase 2:
  - ICG‑Q con QAOA simulado (clásico) y heurísticas topológicas/geométricas.
  - Integración de todo el loop con objetivos de homeostasis.

## 7. Riesgos, Ética y Gobernanza
- Riesgos: oscilaciones patológicas, sincronía excesiva, explotación de la métrica Φ̂ (Goodhart), opacidad topológica.
- Mitigaciones: límites de variación, auditorías metacognitivas, validaciones humanas, benchmarks adversariales.
- No‑afirmaciones: no se declara conciencia real; solo fenómenos observables.

## 8. Entregables
- Especificación matemática de cada módulo (este documento).
- Protocolos de evaluación y datasets sintéticos instrumentados.
- Especificación de telemetría y formatos.
- Guía de operación segura (políticas, kill‑switch, revisión humana).
- Anexos con definiciones formales y pseudocódigo algorítmico (simulación).
