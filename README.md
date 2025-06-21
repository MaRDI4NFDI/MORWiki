# MORWiki

<!-- SPHINX-START -->

A configurable data (and metadata) fetcher for [MORWiki](https://modelreduction.org/morwiki) examples.

Authors:
- Ashwin S. Nayak
  [![orcid](https://img.shields.io/badge/%20-orcid-black?logo=orcid&style=plastic)](https://orcid.org/0000-0002-9855-2377)
  [![github](https://img.shields.io/badge/%20-github-black?logo=github&style=plastic)](https://github.com/ashwin-nayak)
- Jens Saak
  [![orcid](https://img.shields.io/badge/%20-orcid-black?logo=orcid&style=plastic)](https://orcid.org/0000-0001-5567-9637)
  [![github](https://img.shields.io/badge/%20-github-black?logo=github&style=plastic)](https://github.com/drittelhacker)

Affiliation:
- [Max Planck Institute for Dynamics of Complex Technical Systems](https://www.mpi-magdeburg.mpg.de), Magdeburg, Germany.

License:
- BSD 3-Clause, see [`LICENSE`](LICENSE).

Documentation:
[![Documentation Status](https://readthedocs.org/projects/morwiki/badge/?version=latest)](https://morwiki.readthedocs.io/en/latest/?badge=latest)

## Installation

This project relies heavily on `uv`, a fast and efficient tool for managing Python projects and their dependencies. While this is not strictly necessary, it eases the installation process.

> [!tip]
> To install `uv`, check out the [official installation instructions](https://docs.astral.sh/uv/getting-started/installation/) for your platform. Alternatively, you can also install it via `pip`, `pipx`, `brew`, and by downloading the standalone binary.

The following sections provide more details on how to use this project for different purposes.

> [!note]
> For developers (testing, documentation and building), refer to [README.dev.md](README.dev.md).

### Use in your own projects

The project is yet to be published on PyPI, so to install this project as a dependency,

```bash
uv add git+https://github.com/mardi4nfdi/morwiki.git
```

### Run Demos
First clone the repository,

```bash
git clone https://github.com/mardi4nfdi/morwiki.git
cd morwiki
```

Install the required dependencies,

```bash
uv sync
```
This command reads the dependencies from `pyproject.toml` and installs them into a virtual environment, which is created by default in the `.venv` directory.

Subsequently, you can run the demos,

```bash
uv run demos/steel_profile.py
```

## Configuration

`MORWiki` supports flexible configuration through environment variables or a YAML configuration file. See the [configuration guide](CONFIGURE.md) for more details.
