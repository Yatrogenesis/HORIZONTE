from __future__ import annotations

from typing import List, Optional

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from ..core.config import SimConfig
from ..cli import run_episode
from ..mitg.topology import o_information_gaussian
from ..mitg.oinfo import o_information_knn
from ..mitg.iit_discrete import phi_stochastic_interaction
from ..mitg.iit30 import phi_effect_iit30, phi_cause_iit30


app = FastAPI(title="HORIZONTE API", version="0.1.0")


class SimConfigIn(BaseModel):
    n: int = Field(128, ge=2)
    r: float = 3.9
    kappa: float = Field(0.14, ge=0.0, le=0.5)
    noise: float = Field(0.001, ge=0.0)
    steps: int = Field(300, ge=10)
    seed: int = 42
    window: int = Field(50, ge=5)


@app.post("/episodes/start")
def api_run_episode(cfg: SimConfigIn):
    run_episode(SimConfig(**cfg.dict()))
    return {"status": "ok"}


class WindowIn(BaseModel):
    window: List[List[float]]
    knn_k: Optional[int] = 5


@app.post("/metrics/oinfo")
def api_oinfo(payload: WindowIn):
    X = np.asarray(payload.window, dtype=float)
    if X.ndim != 2:
        raise HTTPException(400, detail="window must be 2D")
    mg = o_information_gaussian(X)
    ok, mk = o_information_knn(X, k=int(payload.knn_k or 5))
    return {"gaussian": mg, "knn": {"Oinfo": ok, **mk}}


class TPMIn(BaseModel):
    tpm: List[List[float]]
    p_x: Optional[List[float]] = None


@app.post("/iit/phi_si")
def api_phi_si(payload: TPMIn):
    tp = np.asarray(payload.tpm, dtype=float)
    px = None if payload.p_x is None else np.asarray(payload.p_x, dtype=float)
    phi, part = phi_stochastic_interaction(tp, px)
    return {"phi_si": phi, "partition": [list(part[0]), list(part[1])]}


class IIT30In(BaseModel):
    tpm: List[List[float]]
    mechanism: List[int]
    purview: List[int]
    m_state: List[int]


@app.post("/iit30/effect")
def api_iit30_effect(payload: IIT30In):
    tp = np.asarray(payload.tpm, dtype=float)
    n = int(np.log2(tp.shape[0]) + 1e-9)
    res = phi_effect_iit30(tp, n, payload.mechanism, payload.purview, payload.m_state)
    return {"phi": res.phi, "partition": [list(res.partition[0]), list(res.partition[1]), list(res.partition[2]), list(res.partition[3])], "full": res.full.tolist(), "factored": res.factored.tolist()}


@app.post("/iit30/cause")
def api_iit30_cause(payload: IIT30In):
    tp = np.asarray(payload.tpm, dtype=float)
    n = int(np.log2(tp.shape[0]) + 1e-9)
    res = phi_cause_iit30(tp, n, payload.mechanism, payload.purview, payload.m_state)
    return {"phi": res.phi, "partition": [list(res.partition[0]), list(res.partition[1]), list(res.partition[2]), list(res.partition[3])], "full": res.full.tolist(), "factored": res.factored.tolist()}

