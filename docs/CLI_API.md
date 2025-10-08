# CLI y Contratos de API (Propuesta)

## CLI
- Ejecutar episodio por defecto: `horizonte`
- Parámetros (vía variables en código; próximamente flags):
  - `n` (nodos), `r` (mapa logístico), `kappa`, `noise`, `steps`, `window`, `seed`.
- Salidas: logs JSONL en `logs/` con eventos `SCH`, `MITG`, `AMD`, `ECA`, `ICGQ`, `CTRL`, `REPORT`.

## API (Implementada)
- `POST /episodes/start` → inicia episodio con `SimConfig`.
- `POST /metrics/oinfo` → calcula O-information Gaussiana exacta y kNN.
- `POST /iit/phi_si` → Φ_SI exacta (Stochastic Interaction) para TPM binaria pequeña.
- `POST /iit30/effect` y `/iit30/cause` → IIT 3.0 (repertorios efecto/causa con MIP vía EMD/LP).

Ejemplos (PowerShell / curl)
- O-info (ventana T×N):
  - PowerShell: `Invoke-RestMethod -Uri http://127.0.0.1:8000/metrics/oinfo -Method POST -Body ($body | ConvertTo-Json) -ContentType 'application/json'`
  - curl: `curl -X POST http://127.0.0.1:8000/metrics/oinfo -H 'Content-Type: application/json' -d '{"window": [[0.1,0.2,0.3], ...], "knn_k":5}'`
- Φ_SI:
  - curl: `curl -X POST http://127.0.0.1:8000/iit/phi_si -H 'Content-Type: application/json' -d '{"tpm": [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]}'`
- IIT 3.0 efecto:
  - curl: `curl -X POST http://127.0.0.1:8000/iit30/effect -H 'Content-Type: application/json' -d '{"tpm": [[...]], "mechanism":[0,1], "purview":[1], "m_state":[1,0]}'`

Esquemas detallados en `CONTRATOS_IO.md`.
