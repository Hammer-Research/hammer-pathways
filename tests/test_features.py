import numpy as np
import pytest
from hammer_pathways import mean_rank_features, specimen_ranks


def test_ties_and_constant_specimens():
    np.testing.assert_array_equal(specimen_ranks([[2, 2, 4], [5, 5, 5]]),
                                  [[.25, .25, 1.], [.5, .5, .5]])


def test_sample_locality_and_input_preservation():
    expression=np.array([[1., 2., 3.], [3., 2., 1.]])
    original=expression.copy(); genes=['a','b','c']
    result=mean_rank_features(expression,genes,genes,[[0,1],[1,2]])
    np.testing.assert_array_equal(result,[[.25,.75],[.75,.25]])
    np.testing.assert_array_equal(result[:1],mean_rank_features(expression[:1]*4+8,genes,genes,[[0,1],[1,2]]))
    np.testing.assert_array_equal(expression,original)


@pytest.mark.parametrize('groups', [[],[[]],[[0,0]],[[3]],[[True]],[[1.5]],[[-1]]])
def test_invalid_memberships_fail(groups):
    with pytest.raises(ValueError):mean_rank_features([[1,2,3]],['a','b','c'],['a','b','c'],groups)


@pytest.mark.parametrize('values', [[[1]], [1,2,3], [[1,np.nan]], [[1,np.inf]]])
def test_invalid_matrix_fails(values):
    with pytest.raises(ValueError):specimen_ranks(values)


def test_order_and_identity_are_explicit():
    for genes in [['a','a','c'],['b','a','c'],['a','','c']]:
        with pytest.raises(ValueError):mean_rank_features([[1,2,3]],genes,['a','b','c'],[[0]])
    with pytest.raises(ValueError):mean_rank_features([[1,2]],['a','b','c'],['a','b','c'],[[0]])


def test_empty_sample_axis_preserves_output_width():
    assert mean_rank_features(np.empty((0,3)),['a','b','c'],['a','b','c'],[[0],[1,2]]).shape==(0,2)
