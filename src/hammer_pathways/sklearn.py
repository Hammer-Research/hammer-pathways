"""Optional scikit-learn adapter. SPDX-License-Identifier: MIT."""
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted, validate_data

from .features import mean_rank_features


class MeanRankTransformer(TransformerMixin, BaseEstimator):
    """Compose a fixed gene-set transform with sklearn pipelines.

    ``fit`` validates and freezes the supplied definition; it learns no cohort
    statistics and ignores labels. Memberships must be selected independently
    of held-out outcomes. Arrays use the declared gene order. DataFrame columns
    must match it exactly; a fit with named columns requires named transforms.
    """

    def __init__(self, gene_ids, memberships, *, feature_names=None):
        self.gene_ids = gene_ids
        self.memberships = memberships
        self.feature_names = feature_names

    def _definition(self):
        genes = tuple(self.gene_ids)
        groups = tuple(tuple(group) for group in self.memberships)
        names = (tuple(self.feature_names) if self.feature_names is not None
                 else tuple(f'gene_set_{index}' for index in range(len(groups))))
        return genes, groups, names

    @staticmethod
    def _check_columns(X, genes):
        columns = getattr(X, 'columns', None)
        if columns is not None and list(columns) != list(genes):
            raise ValueError('DataFrame columns must match the declared gene order')

    def fit(self, X, y=None):
        for name in ('gene_ids_', 'memberships_', 'output_names_', 'n_features_in_', 'feature_names_in_'):
            self.__dict__.pop(name, None)
        genes, groups, names = self._definition()
        self._check_columns(X, genes)
        if (len(names) != len(groups) or any(not isinstance(name, str) or not name.strip() for name in names)
                or len(set(names)) != len(names)):
            raise ValueError('Unique output names required, one per gene set')
        values = validate_data(self, X, dtype=float, ensure_min_features=2)
        mean_rank_features(values, genes, genes, groups)
        self.gene_ids_, self.memberships_, self.output_names_ = genes, groups, names
        return self

    def transform(self, X):
        check_is_fitted(self, ['gene_ids_', 'memberships_', 'output_names_'])
        if self._definition() != (self.gene_ids_, self.memberships_, self.output_names_):
            raise ValueError('Feature definition changed; refit the transformer')
        self._check_columns(X, self.gene_ids_)
        if hasattr(self, 'feature_names_in_') and getattr(X, 'columns', None) is None:
            raise ValueError('Named training inputs require named transform inputs')
        # Arrays rely on declared order; named inputs are checked above even
        # when training used arrays and sklearn has no feature_names_in_.
        values = X if hasattr(self, 'feature_names_in_') else np.asarray(X)
        values = validate_data(self, values, reset=False, dtype=float, ensure_min_features=2)
        return mean_rank_features(values, self.gene_ids_, self.gene_ids_, self.memberships_)

    def get_feature_names_out(self, input_features=None):
        check_is_fitted(self, ['gene_ids_', 'output_names_'])
        if input_features is not None and list(input_features) != list(self.gene_ids_):
            raise ValueError('Input feature names must match the declared gene order')
        return np.asarray(self.output_names_, dtype=object)
