<!-- SPHINX-START -->
# Developer Guide

This guide provides instructions for setting up a development environment to contribute to `morb-fetch`.
We recommend using modern, fast tooling like [`uv`](https://astral.sh/uv) and [`nox`](https://nox.thea.codes) to streamline the development process.

## Prerequisites

Before you begin, ensure you have the following tools installed on your system:
- **Git**: For version control.
- **Python**: A recent version (e.g., 3.10+).
- **uv**: A fast Python package installer and resolver. You can install it using the [official installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

## 1. Initial Project Setup

First, clone the repository and navigate into the project directory:
```bash
git clone https://github.com/mardi4nfdi/morb-fetch.git
cd morb-fetch
```

Next, create a virtual environment and install all required dependencies, including development tools, using `uv`:
```bash
uv sync
```
This command reads the `[project.dependencies]` and `[project.optional-dependencies]` from `pyproject.toml` and installs them into a virtual environment, which `uv` creates by default in a `.venv` directory.

To run any demos or scripts use, e.g.
```bash
uv run demos/steel_profile.py
```

## 2. Development Workflow with Nox

We use `nox` to automate common development tasks like running tests, linting, and building documentation. `nox` ensures that these tasks run in clean, isolated environments, providing consistent results.

You can run `nox` without installing it into your global environment by using `uvx`:
```bash
uvx nox
```

### Run everything

To run the full suite of tests for all Python versions available on your system and docs, simply execute:
```bash
nox
```
`nox` will automatically skip sessions for Python versions that are not installed.

### Run Specific Tasks

You can also execute specific `nox` sessions individually.

**Running Tests**
Use `pytest` to execute the unit tests:
```bash
nox -s tests
```

**Building Documentation**
The documentation build is a two-step process. First, build the auto-generated API documentation, then build the main Sphinx site:
```bash
# 1. Generate API documentation from docstrings
nox -s build_api_docs

# 2. Build the HTML documentation
nox -s docs
```
The final documentation will be available in the `docs/_build/html` directory.

**Building the Package**
To create a source distribution (`sdist`) and a binary wheel for the package:
```bash
nox -s build
```
The distributable files will be placed in the `dist/` directory.

## 3. Contributing

We welcome contributions! Please follow these steps to contribute:
1.  Fork the repository on GitHub.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with clear, descriptive messages.
4.  Ensure all tests and linting checks pass by running `nox`.
5.  Push your branch to your fork and open a pull request against the main `morb-fetch` repository.
