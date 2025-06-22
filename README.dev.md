# For Developers

[`nox`](https://nox.thea.codes) is the preferred tool to start with development.
Nox handles everything - including setting up an temporary virtual environment for each run.
To run it without installing use
```bash
uvx nox # (or, uv tool install nox)
```
To test and build docs using every installed version of Python on your system, skipping ones that are not installed, use,
```bash
nox
```
You can also run specific jobs:

Use pytest to run the unit tests,

```bash
nox -s tests  # Python tests
```

Build and serve the docs using:
```bash
nox -s build_api_docs
nox -s docs
```
Make an sdist and wheel,
```bash
nox -s build
```
