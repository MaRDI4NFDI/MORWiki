# MORWiki

<!-- SPHINX-START -->

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

Install the required dependencies using `uv` (recommended),

> Check out the [installation instructions](https://docs.astral.sh/uv/getting-started/installation/) to install `uv` for your platform or via `pip`, `pipx`, `brew`, and just downloading the binary (single file).

```bash
uv sync
```
This will read the dependencies from `pyproject.toml` and install them in a virtual environment. The virtual environment will be created in the `.venv` directory by default.

### Development

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

#### Testing

Use pytest to run the unit checks:

```bash
nox -s tests  # Python tests
```

#### Building docs
You can build and serve the docs using:
```bash
nox -s build_api_docs
nox -s docs
```

You can build the docs only with:
```bash
nox -s docs --non-interactive
```

#### Build distribution
Make an sdist and wheel:
```bash
nox -s build
```

## Configuration

`MORWiki` supports flexible configuration through environment variables or a YAML configuration file.
The precedence for configuration values is as follows (from highest to lowest): environment variables, YAML configuration file, default configuration.
The default values are as follows:

| Property | Value |
| ---------------|-----------|
| Server URL     | `https://csc.mpi-magdeburg.mpg.de/mpcsc/MORB-data/` |
| Indexfile      | `examples.csv` |
| Indexfile hash | `sha256:960a243420e3e2d229bebb26313541841c6d5b51b9f215d7ca7b77c6b3636791` |
| Max Filesize   | `None` |
| Cache Location | OS-specific cache path (`~/.cache/morwiki` for Linux) |

You can override the configuration either by setting environment variables or by using a YAML configuration file.


### Environment Variables

You can override configuration settings using the following environment variables:

- `MORWIKI_SERVERURL`: The base URL for the MorWiki server.
- `MORWIKI_INDEXFILE`: The filename of the index file.
- `MORWIKI_INDEXFILEHASH`: The SHA256 hash of the index file.
- `MORWIKI_MAX_FILESIZE`: The maximum file size allowed for download.
- `MORWIKI_CACHE`: The path to the cache directory.

### Configuration File

In addition to environment variables, configuration can be provided via a YAML file named `morwiki.config.yaml`.
To generate a template configuration file at a specific path (e.g. `/some/path`), run:

```bash
uv run python3 -m morwiki --create-config /some/path
```
If no path is specified, the configuration file will be created in the current working directory.
Using the `--create-config user` option places the file in the user's cache directory.

The configuration file in the working directory takes precedence over the user-level configuration file.
To specify a custom configuration file located elsewhere, set the `MORWIKI_CONFIG_FILE` environment variable:
```bash
export MORWIKI_CONFIG_FILE=/path/to/config.yaml
```

### View active configuration

To print the active configuration, run:

```bash
uv run python3 -m morwiki --print-config
```
