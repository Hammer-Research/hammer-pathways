# Contributing

Start with a small synthetic example. No cancer dataset, private repository access or paid service is needed.

## Development

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[test]'
python -m pytest tests -q
python examples/minimal.py
```

## Useful contributions

- Report a numerical discrepancy with the input, expected mathematical result, actual result, package version and Python/NumPy/SciPy versions.
- Add a composability example that uses the public functions without changing the API.
- Improve a confusing contract or error message with a test when behavior changes.

For a larger API or algorithm change, open an issue first with the use case and alternatives. Keep gene-universe selection explicit; no implicit matching or imputation. Explain whether outputs change. Do not mix numerical changes with unrelated formatting. New dependencies need a concrete use case.

Open a pull request with the problem, change and test results. Use the MIT license for contributions to this package. Preserve attribution for third-party material; do not submit datasets, credentials or patient information. Disclose AI assistance and verify generated code yourself. A maintainer reviews changes before merging; no response deadline is promised.

Release checks install a built wheel on Python 3.10, 3.12 and 3.14, run tests and the synthetic example, and verify that importing the library does not import Hammer's research engine or training frameworks. Passing tests establish software behavior, not clinical validity.

## Credit

Accepted contributions retain Git authorship. Describe substantive work in the release notes and use the contributor's preferred name when agreed. Contribution does not promise research-paper authorship. Challenge methods respectfully and provide reproducible evidence.
