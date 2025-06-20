# MORWiki

<!-- SPHINX-START -->

Fetches data (and metadata) from MORWiki Examples

Authors:
- **Ashwin S. Nayak**
  [![orcid](https://img.shields.io/badge/%20-orcid-black?logo=orcid&style=plastic)](https://orcid.org/0000-0002-9855-2377)
  [![gitlab](https://img.shields.io/badge/%20-gitlab-black?logo=gitlab&style=plastic)](https://gitlab.mpi-magdeburg.mpg.de/anayak)
  [![github](https://img.shields.io/badge/%20-github-black?logo=github&style=plastic)](https://github.com/ashwin-nayak)
- **Jens Saak**
  [![orcid](https://img.shields.io/badge/%20-orcid-black?logo=orcid&style=plastic)](https://orcid.org/0000-0001-5567-9637)
  [![gitlab](https://img.shields.io/badge/%20-gitlab-black?logo=gitlab&style=plastic)](https://gitlab.mpi-magdeburg.mpg.de/saak)
  [![github](https://img.shields.io/badge/%20-github-black?logo=github&style=plastic)](https://github.com/drittelhacker)

Affiliation:
  - [Max Planck Institute for Dynamics of Complex Technical Systems](https://www.mpi-magdeburg.mpg.de), Magdeburg, Germany.

License:
  - BSD 3-Clause, see [`LICENSE`](LICENSE).

Documentation:
  - [Gitlab Pages](http://morwiki-515d88.pages.csc.mpi-magdeburg.mpg.de/index.html) (currently, only available internally within institute)

## Installation

This project relies heavily on `uv`, a fast and efficient tool for managing Python projects and their dependencies.

> [!tip]
> To install `uv`, check out the [official installation instructions](https://docs.astral.sh/uv/getting-started/installation/) for your platform. Alternatively, you can also install it via `pip`, `pipx`, `brew`, and by downloading the standalone binary.

The following sections provide more details on how to use this project for different purposes.

> [!note]
> For developers (testing, documentation and building), refer to [README.dev.md](README.dev.md).

### Run Demos
First clone the repository

```bash
git clone https://gitlab.mpi-magdeburg.mpg.de/mardi/morwiki.git
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

### Use in your own projects

To install this project as a dependency,

```bash
uv add git+https://gitlab.mpi-magdeburg.mpg.de/mardi/morwiki.git
```

## Configuration

`MORWiki` supports flexible configuration through environment variables or a YAML configuration file. See the [configuration guide](CONFIGURE.md) for more details.
