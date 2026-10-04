"""Synthetic example: no patient data, network, credentials or model needed."""
import numpy as np
from hammer_pathways import mean_rank_features

genes = ['gene-a', 'gene-b', 'gene-c']
expression = [[1., 2., 3.], [3., 2., 1.]]
features = mean_rank_features(expression, genes, genes, [[0, 1], [1, 2]])
np.testing.assert_array_equal(features, [[.25, .75], [.75, .25]])
print(features)
