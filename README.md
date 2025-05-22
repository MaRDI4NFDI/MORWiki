# MORWiki

Fetches data (and metadata) from MORWiki Examples

Authors:
- **Ashwin S. Nayak**
  [![orcid](https://img.shields.io/badge/%20-orcid-black?logo=orcid&style=plastic)](https://orcid.org/0000-0002-9855-2377)
  [![github](https://img.shields.io/badge/%20-gitlab-black?logo=gitlab&style=plastic)](https://gitlab.mpi-magdeburg.mpg.de/anayak)
- **Jens Saak**
  [![orcid](https://img.shields.io/badge/%20-orcid-black?logo=orcid&style=plastic)](https://orcid.org/0000-0001-5567-9637)
  [![github](https://img.shields.io/badge/%20-gitlab-black?logo=gitlab&style=plastic)](https://gitlab.mpi-magdeburg.mpg.de/saak)

Affiliation:
  - [Max Planck Institute for Dynamics of Complex Technical Systems](https://www.mpi-magdeburg.mpg.de), Magdeburg, Germany.

License:
  - BSD 3-Clause, see [`LICENSE`](LICENSE).

## Installation

### Getting started
First clone the repository

```bash
git clone https://gitlab.mpi-magdeburg.mpg.de/anayak/morwiki.git
cd morwiki
```

Install the required dependencies using `uv` (Recommended),

> If you don't have `uv` installed, check out the [installation instructions](https://docs.astral.sh/uv/getting-started/installation/) for your platform.

```bash
uv sync
```
This will read the dependencies from `pyproject.toml` and install them in a virtual environment. The virtual environment will be created in the `.venv` directory by default.
