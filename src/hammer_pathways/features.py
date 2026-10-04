"""Deterministic, sample-local numerical transforms. SPDX-License-Identifier: MIT."""
from collections.abc import Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.stats import rankdata


def specimen_ranks(expression: ArrayLike) -> NDArray[np.float64]:
    """Average-tie ranks scaled to [0, 1], separately for each sample row.

    Require finite samples-by-genes input with at least two genes. Does not
    impute, learn cohort parameters, or change the input array. An empty sample
    axis is supported and returns shape (0, number_of_genes).
    """
    values = np.asarray(expression, dtype=float)
    if values.ndim != 2 or values.shape[1] < 2 or not np.isfinite(values).all():
        raise ValueError('Finite sample-by-gene matrix with at least two genes required')
    return (rankdata(values, axis=1, method='average') - 1) / (values.shape[1] - 1)


def mean_rank_features(
    expression: ArrayLike,
    gene_ids: Sequence[str],
    expected_gene_ids: Sequence[str],
    memberships: Sequence[Sequence[int]],
) -> NDArray[np.float64]:
    """Mean specimen rank per gene set, preserving supplied membership order.

    Gene IDs must exactly match a frozen, unique ordered universe. Memberships
    are nonempty sets of zero-based gene-column indexes. Each gene occurs at
    most once per set; different sets may overlap. No gene matching, fitting,
    enrichment statistics or pathway activity inference is performed here.
    """
    genes = list(gene_ids)
    if (any(not isinstance(gene, str) or not gene.strip() for gene in genes)
            or len(set(genes)) != len(genes) or genes != list(expected_gene_ids)):
        raise ValueError('Exact unique gene universe and order required')
    groups = [list(group) for group in memberships]
    if not groups:
        raise ValueError('At least one gene set required')
    for group in groups:
        if (not group or any(type(index) is not int or not 0 <= index < len(genes) for index in group)
                or len(set(group)) != len(group)):
            raise ValueError('Gene-set indexes must be unique integers within the gene universe')
    ranks = specimen_ranks(expression)
    if ranks.shape[1] != len(genes):
        raise ValueError('Gene width mismatch')
    return np.column_stack([ranks[:, group].mean(axis=1) for group in groups])
