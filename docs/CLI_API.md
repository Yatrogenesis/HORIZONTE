# CLI y Contratos de API (Propuesta)

## CLI
- Ejecutar episodio por defecto: `horizonte`
- Parámetros (vía variables en código; próximamente flags):
  - `n` (nodos), `r` (mapa logístico), `kappa`, `noise`, `steps`, `window`, `seed`.
- Salidas: logs JSONL en `logs/` con eventos `SCH`, `MITG`, `AMD`, `ECA`, `ICGQ`, `CTRL`, `REPORT`.

## API (Contrato futuro)
- `POST /episodes/start` → inicia episodio con `SimConfig`.
- `GET /episodes/{id}/telemetry` → stream de eventos JSONL.
- `POST /control/apply` → aplica cambios `{dkappa, dsigma, dg}` con políticas de seguridad.
- `GET /metrics/phi` → últimos valores de Φ̂ y barcodes exportados.

Esquemas detallados en `CONTRATOS_IO.md`.

