# Especificación de Telemetría

## Formato
- JSON Lines (una decisión/evento por línea), UTF‑8.
- Nombre de archivo: `YYYYMMDD_session01.jsonl`.

## Campos Comunes
- `ts` (ms epoch), `module` (SCH|MITG|AMD|ECA|ICGQ|CTRL|REPORT), campos específicos del evento.

## Ejemplos
- SCH: `{ ts, module:'SCH', t, mean, std }`
- MITG: `{ ts, module:'MITG', phi_hat, m_Q, m_participation }`
- AMD: `{ ts, module:'AMD', rho_K }`
- CTRL: `{ ts, module:'CTRL', t, kappa, noise, r, phi }`

## Retención y Privacidad
- TTL configurable, compresión por impacto en Φ̂, minimización de datos, sin PII.

