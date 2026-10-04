"""Synthetic pipeline wiring, not a cancer-detection experiment."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from hammer_pathways.sklearn import MeanRankTransformer

X = np.tile([[1., 2., 3.], [3., 2., 1.]], (6, 1))
y = np.tile([0, 1], 6)
pipeline = Pipeline([
    ('pathways', MeanRankTransformer(['a', 'b', 'c'], [[0, 1], [1, 2]])),
    ('classifier', LogisticRegression()),
])
scores = cross_val_score(pipeline, X, y, cv=StratifiedKFold(3), error_score='raise')
assert len(scores) == 3 and np.isfinite(scores).all()
print('Synthetic pipeline executed across three folds. No biomedical performance claim.')
