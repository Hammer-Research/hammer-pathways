import numpy as np
import pytest

pytest.importorskip('sklearn')
from sklearn.base import clone
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from hammer_pathways import mean_rank_features
from hammer_pathways.sklearn import MeanRankTransformer


def transformer():
    return MeanRankTransformer(['a','b','c'], [[0,1],[1,2]], feature_names=['first','second'])


def test_clone_and_function_equivalence():
    original=transformer(); fitted=clone(original).fit([[1,2,3],[3,2,1]])
    with pytest.raises(NotFittedError):original.transform([[1,2,3]])
    actual=fitted.transform([[1,2,3]])
    np.testing.assert_array_equal(actual, mean_rank_features([[1,2,3]],['a','b','c'],['a','b','c'],[[0,1],[1,2]]))
    assert fitted.n_features_in_==3
    assert fitted.get_feature_names_out().tolist()==['first','second']


def test_fit_learns_no_cohort_statistics_or_labels():
    a=transformer().fit([[1,2,3],[3,2,1]],[0,1])
    b=transformer().fit([[8,8,8],[100,2,-100]],[1,0])
    np.testing.assert_array_equal(a.transform([[4,5,6]]), b.transform([[4,5,6]]))


def test_pipeline_cross_validation():
    X=np.tile([[1,2,3],[3,2,1]],(6,1)); y=np.tile([0,1],6)
    pipeline=Pipeline([('features',transformer()),('classifier',LogisticRegression())])
    scores=cross_val_score(pipeline,X,y,cv=StratifiedKFold(3),error_score='raise')
    assert scores.shape==(3,) and np.isfinite(scores).all()


def test_changed_definition_requires_refit():
    model=transformer().fit([[1,2,3]])
    model.memberships[0].append(2)
    with pytest.raises(ValueError,match='refit'):model.transform([[1,2,3]])
    model.fit([[1,2,3]])
    assert model.transform([[1,2,3]])[0,0]==.5


def test_failed_refit_invalidates_old_fit():
    model=transformer().fit([[1,2,3]])
    with pytest.raises(ValueError):model.fit([[np.nan,2,3]])
    with pytest.raises(NotFittedError):model.transform([[1,2,3]])


@pytest.mark.parametrize('names',[['duplicate','duplicate'],['one'],['','two']])
def test_invalid_output_names(names):
    with pytest.raises(ValueError):MeanRankTransformer(['a','b','c'],[[0],[1]],feature_names=names).fit([[1,2,3]])


def test_named_columns_and_dataframe_output():
    pd=pytest.importorskip('pandas')
    frame=pd.DataFrame([[1,2,3]],columns=['a','b','c'])
    model=transformer().set_output(transform='pandas').fit(frame)
    assert model.transform(frame).columns.tolist()==['first','second']
    with pytest.raises(ValueError,match='order'):model.transform(frame[['b','a','c']])
    with pytest.raises(ValueError,match='named'):model.transform(frame.to_numpy())
    with pytest.raises(ValueError,match='order'):transformer().fit(frame[['b','a','c']])


def test_array_fit_accepts_correctly_named_transform():
    pd=pytest.importorskip('pandas')
    model=transformer().fit([[1,2,3]])
    np.testing.assert_array_equal(model.transform(pd.DataFrame([[1,2,3]],columns=['a','b','c'])),[[.25,.75]])
    with pytest.raises(ValueError):model.get_feature_names_out(['c','b','a'])
