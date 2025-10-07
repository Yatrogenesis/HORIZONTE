# Contratos de Entrada/Salida (Esquemas)

## Evento episódico
```
{ id, ts, modulo, entrada, salida, confianza?, notas? }
```

## Estado del Yo (self‑model)
```
{ identidad, capacidades, limitaciones, metas_activas, nivel_confianza }
```

## Métrica
```
{ nombre, valor, ventana, objetivo }
```

## Control (actuadores SCH)
```
{ dkappa, dsigma, dg, dA_sparsify? }
```

Todas las estructuras se serializan en JSON y se trazan vía `TELEMETRIA_SPEC.md`.

