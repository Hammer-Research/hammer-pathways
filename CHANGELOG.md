# Changelog

## 0.2.0

- Add optional `MeanRankTransformer` for scikit-learn pipelines and cross-validation.
- Validate named columns, expose output feature names, freeze feature definitions
  at fit, and require refitting after parameter mutation.
- Keep base NumPy/SciPy imports and numerical functions unchanged.
- Add synthetic pipeline and DataFrame integration checks. No research model
  coefficients, cutoff or validation claims changed.

## 0.1.0

- Extract specimen-local average ranks and mean gene-set ranks into a standalone NumPy/SciPy package.
- Require explicit ordered gene identifiers and gene-set indexes.
- Reject duplicate, empty, boolean and out-of-range membership indexes.
- Provide type annotations, synthetic examples and numerical boundary tests.
- MIT license applies to this package only. No models or source datasets are included.

Integration verification reproduced all 45 stored development fitted scores exactly. This is numerical equivalence, not independent clinical performance.
