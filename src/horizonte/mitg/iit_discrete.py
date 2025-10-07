from __future__ import annotations

import itertools
from typing import Iterable, List, Sequence, Tuple

import numpy as np


def _all_bipartitions(n: int) -> Iterable[Tuple[Tuple[int, ...], Tuple[int, ...]]]:
    idxs = list(range(n))
    for r in range(1, n // 2 + 1):
        for A in itertools.combinations(idxs, r):
            B = tuple(i for i in idxs if i not in A)
            # avoid duplicates by enforcing min element in A < min element in B
            if A and B and A[0] < B[0]:
                yield (tuple(A), B)


def _bits_to_index(bits: Sequence[int]) -> int:
    idx = 0
    for b in bits:
        idx = (idx << 1) | (b & 1)
    return idx


def _index_to_bits(idx: int, n: int) -> List[int]:
    return [((idx >> (n - 1 - j)) & 1) for j in range(n)]


def stationary_uniform(n: int) -> np.ndarray:
    p = np.ones(2**n, dtype=float) / (2**n)
    return p


def marginalize_conditional(tp: np.ndarray, n: int, block: Sequence[int]) -> np.ndarray:
    """Return p(x'_block | x_block) by summing out other variables.

    Args:
      tp: shape (2^n, 2^n) conditional p(x'|x) (rows x, cols x')
      block: indices of variables in the block
    Returns:
      array shape (2^{|block|}, 2^{|block|}) mapping x_block -> x'_block
    """
    all_vars = tuple(range(n))
    other = [i for i in all_vars if i not in block]
    m = len(block)
    out = np.zeros((2**m, 2**m), dtype=float)
    # iterate over x (all states), sum probability mass mapping to x'_block states
    for x in range(2**n):
        xb = _bits_to_index([_index_to_bits(x, n)[i] for i in block])
        row = tp[x]  # distribution over x'
        # sum probability per x'_block
        mass_block = np.zeros(2**m, dtype=float)
        for xp in range(2**n):
            xpb = _bits_to_index([_index_to_bits(xp, n)[i] for i in block])
            mass_block[xpb] += row[xp]
        out[xb] += mass_block
    # normalize rows (for each x_block)
    out = out / (out.sum(axis=1, keepdims=True) + 1e-15)
    return out


def phi_stochastic_interaction(tp: np.ndarray, p_x: np.ndarray | None = None) -> Tuple[float, Tuple[Tuple[int, ...], Tuple[int, ...]]]:
    """Integrated information via Stochastic Interaction (Ay & Polani) exact for discrete Markov systems.

    Phi_SI = min_{bipartitions P} E_{p(x)} [ D_KL( p(x'|x) || \prod_{B in P} p(x'_B | x_B) ) ]

    Args:
      tp: conditional p(x'|x) shape (2^n, 2^n), rows sum to 1
      p_x: distribution over x (2^n). If None, uses uniform.
    Returns:
      (phi_value, argmin_partition)
    """
    if tp.ndim != 2 or tp.shape[0] != tp.shape[1]:
        raise ValueError("TPM must be square (2^n, 2^n)")
    n_states = tp.shape[0]
    n = int(np.log2(n_states) + 1e-9)
    if 2**n != n_states:
        raise ValueError("TPM size must be power of 2 for binary variables")
    if p_x is None:
        p_x = np.ones(n_states, dtype=float) / n_states
    # validate
    if not np.allclose(tp.sum(axis=1), 1.0, atol=1e-8):
        raise ValueError("Each row of TPM must sum to 1")
    if not np.isclose(np.sum(p_x), 1.0, atol=1e-8):
        raise ValueError("p_x must sum to 1")

    # Precompute block conditionals for each candidate block set
    best_phi = float("inf")
    best_P: Tuple[Tuple[int, ...], Tuple[int, ...]] | None = None
    for A, B in _all_bipartitions(n):
        tp_A = marginalize_conditional(tp, n, A)
        tp_B = marginalize_conditional(tp, n, B)
        # KL for each x: D_KL( p(.|x) || prod_B p_B(.|x_B) )
        kl_sum = 0.0
        for x in range(n_states):
            px = p_x[x]
            if px <= 0.0:
                continue
            p_row = tp[x]  # shape (2^n,)
            # build product distribution over x' by Kronecker of block conditionals given x_A and x_B
            xA = _bits_to_index([_index_to_bits(x, n)[i] for i in A])
            xB = _bits_to_index([_index_to_bits(x, n)[i] for i in B])
            pA = tp_A[xA]  # (2^|A|,)
            pB = tp_B[xB]  # (2^|B|,)
            p_fact = np.kron(pA, pB)  # (2^n,)
            # KL
            mask = (p_row > 0) & (p_fact > 0)
            dkl = np.sum(p_row[mask] * (np.log(p_row[mask]) - np.log(p_fact[mask])))
            kl_sum += px * dkl
        if kl_sum < best_phi:
            best_phi = kl_sum
            best_P = (A, B)
    assert best_P is not None
    return float(best_phi), best_P


def tpm_identity(n: int) -> np.ndarray:
    """TPM for identity update x' = x (deterministic)."""
    tp = np.zeros((2**n, 2**n), dtype=float)
    for x in range(2**n):
        tp[x, x] = 1.0
    return tp


def tpm_xor_chain() -> np.ndarray:
    """Example 2-bit TPM with x1' = x1, x2' = x1 XOR x2 (deterministic)."""
    n = 2
    tp = np.zeros((4, 4), dtype=float)
    for x in range(4):
        b = _index_to_bits(x, 2)
        x1, x2 = b[0], b[1]
        x1p = x1
        x2p = x1 ^ x2
        xp = _bits_to_index([x1p, x2p])
        tp[x, xp] = 1.0
    return tp

