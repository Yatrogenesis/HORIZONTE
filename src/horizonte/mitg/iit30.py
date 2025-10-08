from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

import numpy as np
from scipy.optimize import linprog


def bits_to_index(bits: Sequence[int]) -> int:
    idx = 0
    for b in bits:
        idx = (idx << 1) | (b & 1)
    return idx


def index_to_bits(idx: int, n: int) -> List[int]:
    return [((idx >> (n - 1 - j)) & 1) for j in range(n)]


def enumerate_states(n: int) -> List[List[int]]:
    return [index_to_bits(i, n) for i in range(2**n)]


def all_nontrivial_bipartitions(idx: Tuple[int, ...]) -> Iterable[Tuple[Tuple[int, ...], Tuple[int, ...]]]:
    k = len(idx)
    if k < 2:
        return []
    for r in range(1, k // 2 + 1):
        for A in itertools.combinations(idx, r):
            B = tuple(i for i in idx if i not in A)
            if A and B and A[0] < B[0]:
                yield (tuple(A), B)


def project_distribution(full: np.ndarray, n: int, P: Sequence[int]) -> np.ndarray:
    """Project distribution over all N bits to distribution over bits in P.
    full: shape (2^N,), entries sum to 1.
    Returns array shape (2^{|P|},).
    """
    k = len(P)
    out = np.zeros(2**k, dtype=float)
    for xp in range(2**n):
        bits = index_to_bits(xp, n)
        proj_bits = [bits[i] for i in P]
        j = bits_to_index(proj_bits)
        out[j] += full[xp]
    return out


def effect_repertoire(tp: np.ndarray, n: int, M: Sequence[int], P: Sequence[int], m_state: Sequence[int]) -> np.ndarray:
    """p(s_P' | do(x_M = m_state)) by averaging over unconstrained variables in x with uniform prior, then TPM, then projecting to P.
    tp: (2^n, 2^n) rows x, cols x'.
    Returns array shape (2^{|P|},) that sums to 1.
    """
    # accumulate p(x'|do(m)) by averaging rows of TPM for all x consistent with m
    unconstrained_idx = [i for i in range(n) if i not in M]
    p_xp = np.zeros(2**n, dtype=float)
    for mask_val in range(2**len(unconstrained_idx)):
        # build x consistent with m on M and mask_val on others
        x_bits = [0] * n
        for mi, bit in zip(M, m_state):
            x_bits[mi] = int(bit)
        other_bits = index_to_bits(mask_val, len(unconstrained_idx))
        for pos, bit in zip(unconstrained_idx, other_bits):
            x_bits[pos] = int(bit)
        x_idx = bits_to_index(x_bits)
        p_xp += tp[x_idx]
    p_xp /= (2 ** len(unconstrained_idx))
    # project to P
    return project_distribution(p_xp, n, P)


def cause_repertoire(tp: np.ndarray, n: int, M: Sequence[int], P: Sequence[int], m_state: Sequence[int]) -> np.ndarray:
    """p(s_P^{t-1} | x_M^{t} = m_state) using Bayes with uniform prior over past states.
    Returns array shape (2^{|P|},).
    """
    # posterior over past full x given current mechanism bits m_state
    # likelihood L(x_prev) = sum_{x'} 1[x'_M = m_state] * p(x'|x_prev)
    L = np.zeros(2**n, dtype=float)
    for x_prev in range(2**n):
        row = tp[x_prev]
        mass = 0.0
        for xp in range(2**n):
            bits = index_to_bits(xp, n)
            ok = True
            for mi, bit in zip(M, m_state):
                if bits[mi] != int(bit):
                    ok = False
                    break
            if ok:
                mass += row[xp]
        L[x_prev] = mass
    if L.sum() == 0.0:
        # degenerate TPM; fallback to uniform
        post = np.ones_like(L) / L.size
    else:
        post = L / L.sum()
    # project to purview in the past
    return project_distribution(post, n, P)


def hamming_cost_matrix(k: int) -> np.ndarray:
    states = enumerate_states(k)
    C = np.zeros((2**k, 2**k), dtype=float)
    for i, a in enumerate(states):
        for j, b in enumerate(states):
            C[i, j] = sum(1 for aa, bb in zip(a, b) if aa != bb)
    return C


def emd_distance(p: np.ndarray, q: np.ndarray, C: np.ndarray) -> float:
    """Earth Mover's Distance (W1) via linear programming.
    p, q shape (m,), sum to 1. C shape (m, m) non-negative costs.
    """
    m = p.size
    A_eq = []
    b_eq = []
    # row sums equal p
    for i in range(m):
        row = np.zeros(m * m)
        row[i * m : (i + 1) * m] = 1.0
        A_eq.append(row)
        b_eq.append(p[i])
    # column sums equal q
    for j in range(m):
        col = np.zeros(m * m)
        col[j::m] = 1.0
        A_eq.append(col)
        b_eq.append(q[j])
    A_eq = np.array(A_eq)
    b_eq = np.array(b_eq)
    c = C.reshape(-1)
    bounds = [(0, None)] * (m * m)
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if not res.success:
        raise RuntimeError(f"linprog failed: {res.message}")
    return float(res.fun)


@dataclass
class PhiResult:
    phi: float
    partition: Tuple[Tuple[int, ...], Tuple[int, ...], Tuple[int, ...], Tuple[int, ...]]
    full: np.ndarray
    factored: np.ndarray


def phi_effect_iit30(tp: np.ndarray, n: int, M: Sequence[int], P: Sequence[int], m_state: Sequence[int]) -> PhiResult:
    full = effect_repertoire(tp, n, M, P, m_state)
    k = len(P)
    C = hamming_cost_matrix(k)
    best = None
    M = tuple(M)
    P = tuple(P)
    for MA, MB in all_nontrivial_bipartitions(M) or [()]:
        for PA, PB in all_nontrivial_bipartitions(P) or [()]:
            if not MA or not MB or not PA or not PB:
                continue
            # compute factored repertoire: p(PA|MA) ⊗ p(PB|MB)
            fA = effect_repertoire(tp, n, MA, PA, [m_state[M.index(i)] for i in MA])
            fB = effect_repertoire(tp, n, MB, PB, [m_state[M.index(i)] for i in MB])
            fact = np.kron(fA, fB)
            dist = emd_distance(full, fact, C)
            if (best is None) or (dist < best[0]):
                best = (dist, (MA, MB, PA, PB), fact)
    if best is None:
        # no nontrivial partition; phi = 0
        return PhiResult(0.0, (tuple(M), tuple(), tuple(P), tuple()), full, full)
    return PhiResult(float(best[0]), best[1], full, best[2])


def phi_cause_iit30(tp: np.ndarray, n: int, M: Sequence[int], P: Sequence[int], m_state: Sequence[int]) -> PhiResult:
    full = cause_repertoire(tp, n, M, P, m_state)
    k = len(P)
    C = hamming_cost_matrix(k)
    best = None
    M = tuple(M)
    P = tuple(P)
    for MA, MB in all_nontrivial_bipartitions(M) or [()]:
        for PA, PB in all_nontrivial_bipartitions(P) or [()]:
            if not MA or not MB or not PA or not PB:
                continue
            fA = cause_repertoire(tp, n, MA, PA, [m_state[M.index(i)] for i in MA])
            fB = cause_repertoire(tp, n, MB, PB, [m_state[M.index(i)] for i in MB])
            fact = np.kron(fA, fB)
            dist = emd_distance(full, fact, C)
            if (best is None) or (dist < best[0]):
                best = (dist, (MA, MB, PA, PB), fact)
    if best is None:
        return PhiResult(0.0, (tuple(M), tuple(), tuple(P), tuple()), full, full)
    return PhiResult(float(best[0]), best[1], full, best[2])


def phi_concept(tp: np.ndarray, n: int, M: Sequence[int], P: Sequence[int], m_state: Sequence[int]) -> Tuple[float, PhiResult, PhiResult]:
    eff = phi_effect_iit30(tp, n, M, P, m_state)
    cau = phi_cause_iit30(tp, n, M, P, m_state)
    return min(eff.phi, cau.phi), eff, cau

