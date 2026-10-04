# Changelog

## 0.1.0

- Extract specimen-local average ranks and mean gene-set ranks into a standalone NumPy/SciPy package.
- Require explicit ordered gene identifiers and gene-set indexes.
- Reject duplicate, empty, boolean and out-of-range membership indexes.
- Provide type annotations, synthetic examples and numerical boundary tests.
- MIT license applies to this package only. No models or source datasets are included.

Integration verification reproduced all 45 stored development fitted scores exactly. This is numerical equivalence, not independent clinical performance.
