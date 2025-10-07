# Especificación Matemática y Algorítmica – HORIZONTE

## 1. SCH: Dinámica Caótica y Control al Borde del Caos
- Red de osciladores acoplados (ej. Rössler/Lorenz):
  x_i' = f(x_i) + κ ∑_j A_{ij} (x_j - x_i) + ξ_i(t)
  con f caótico, κ acoplamiento, A topología, ξ ruido.
- CML (mapas logísticos):
  x_i[t+1] = (1-κ) f(x_i[t]) + κ ⟨ f(x_j[t]) ⟩_{j∈N(i)}, f(x)= r x(1-x)
- Sincronización parcial (Kuramoto):
  θ_i' = ω_i + (K/N) ∑_j A_{ij} sin(θ_j - θ_i)
- Lyapunov máximo λ₁ (Wolf/Benettin): perturbación δx evolucionada, re‑ortogonalización, λ₁ ≈ ⟨ (1/Δt) ln ||δx_{t+Δt}||/||δx_t|| ⟩
- Objetivo crítico: λ₁ ≈ 0⁺, metastabilidad (evitar sincronía total o caos profundo).

## 2. MIT-G: Φ^, Topología Persistente y Grafos
- Embedding (Takens) y grafos funcionales G_t (MI/TE/coherencia).
- Homología persistente (Vietoris-Rips/Alpha): barcodes con Betti β_k; estabilidad por teorema de estabilidad.
- Φ proxies:
  - O-information Ω(X) = ∑_i I(X_i;X_{-i}) − (n−2)I_total (signo separa sinergia vs redundancia)
  - PID/ΦID: descomposición de información en redundante/única/sinérgica; Φ^ = Σ sinergia(C) − penalizaciones por cortes de baja pérdida.
- Métricas de red: Q (modularidad), participation coefficient, k‑core, espectro Laplaciano.

## 3. AMD: EDMD/Koopman y Control MPC
- Levantamiento φ(z): z_t = [métricas MIT-G, resúmenes SCH]
- EDMD: K = (G^+) A, con G = Φ(Z)^T Φ(Z), A = Φ(Z)^T Φ(Z⁺)
- Predicción: φ(z_{t+1}) ≈ K φ(z_t); radio espectral ρ(K) como indicador de bifurcación.
- Señales de alerta: critical slowing down (ACF→1), varianza ↑, curtosis/asimetría, λ₁ ↑, ρ(K)→1.
- MPC: max_u E[ Σ_{h=0..H} ( Φ^_{t+h} − α·riesgo − β·costo ) ] s.a. dinámica Koopman y límites (κ,σ,g,A, umbrales).

## 4. ECA: MARL y Mercado de Atención
- Estado s_i: vecindad en G_t, persistencia local, gradiente de atención, presupuesto.
- Acciones a_i: re‑cableo local, modulación de pesos, inyección de patrones, pujas por atención.
- Recompensa r_i = α·ΔΦ^_global + β·Estabilidad_homeo − γ·Coste_recursos − δ·Penalización_seguridad
- Asignación de crédito: aprox. Shapley/leave‑one‑out sobre ΔΦ^ de coaliciones.
- Dinámica replicadora para asignación de recursos/atención y presión evolutiva (mutación/selección) suave.

## 5. ICG-Q: Optimización Geo‑Cuántica
- Variables: A (aristas), θ = {κ,g,σ}, layouts.
- Costo: C(A,θ) = −Φ^(A,θ) + λ·R_hardware + μ·R_riesgo
- Mapeo cuántico: H_C ↔ C; QAOA/VQE con ansatz guiado por tensor geométrico cuántico (Fisher) para evitar barren plateaus.
- Heurísticas topológicas: prior sobre subgrafos con barcodes persistentes; invariantes de nudos (Jones/Alexander) como robustez estructural.

## 6. Telemetría y Seguridad
- Logs JSONL por módulo; snapshots del self‑model; gatillos de kill‑switch.
