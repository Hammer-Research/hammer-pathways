# hammer-pathways

Small, deterministic functions for within-specimen gene ranks and mean-rank gene-set features. Use them with your own expression matrix and frozen gene-set definition, independently of Hammer Research's website, databases or classifiers.

This is feature engineering, not a pathway enrichment test, pathway activity estimate or diagnostic model. No data or model weights are bundled. The library never downloads data, trains a model, reads credentials or starts a background service.

## Install and run

From a standalone checkout of this package:

```sh
python -m pip install '.[test]'
python examples/minimal.py
python -m pytest tests -q
```

The package is not published on PyPI. Inside the Hammer Research workspace, first run `cd packages/hammer-pathways`.

```python
from hammer_pathways import mean_rank_features

genes = ['a', 'b', 'c']
features = mean_rank_features(
    [[1., 2., 3.], [3., 2., 1.]],
    gene_ids=genes,
    expected_gene_ids=genes,
    memberships=[[0, 1], [1, 2]],
)
# [[0.25, 0.75], [0.75, 0.25]]
```

## Contract

- Input is a finite samples-by-genes array. At least two genes are required; zero samples are allowed.
- Ranks are computed independently per specimen, with average ranks for ties, then scaled by `(rank - 1) / (gene_count - 1)`.
- Gene identifiers must match the expected unique ordered universe exactly. No missing-gene substitution or automatic reordering.
- Memberships are nonempty lists of unique Python integer column indexes. Sets may overlap. Output columns follow supplied membership order.
- Output is a NumPy floating-point matrix. Input is not modified. No cohort-level parameters are learned.
- Invalid inputs raise `ValueError`. Incompatible Python argument types may raise `TypeError`.

Select the gene universe before ranking. Ranking a larger matrix and then dropping genes is a different transform. This library does not establish assay compatibility or patient independence.

## Integration and provenance

Compose these functions with your own data loading, sklearn estimator or reporting code. NumPy and SciPy are the only runtime dependencies. Freeze the gene order, memberships, input hashes, package version and environment with each experiment. No application framework or plugin protocol is required.

Version 0.1.0 is an initial API. Numerical changes must be documented and regression-tested; minor versions may change the API before 1.0. Historical artifacts retain their original provenance.

## Contribute

Useful contributions include a reproducible numerical bug, a missing input boundary check, or an independently reproduced example. Include the smallest synthetic input, expected output with its mathematical basis, actual output and dependency versions. Run the tests and explain numerical changes. No patient data are needed.

See [CONTRIBUTING.md](CONTRIBUTING.md) for local setup and review expectations. This package is MIT-licensed; see LICENSE. The license applies to this package's code and documentation, not to model weights, third-party gene sets or the parent repository. Source data remain subject to their own terms.
