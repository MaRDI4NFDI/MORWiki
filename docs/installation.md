# Installation

This project relies heavily on `uv`, a fast and efficient tool for managing Python projects and their dependencies. While this is not strictly necessary, it eases the installation process.

:::{tip}
To install `uv`, check out the [official installation instructions](https://docs.astral.sh/uv/getting-started/installation/) for your platform. Alternatively, you can also install it via `pip`, `pipx`, `brew`, and by downloading the standalone binary.
:::

The following sections provide more details on how to use this project for different purposes.

:::{note}
For developers (testing, documentation and building), refer to {ref}`developer notes <id-dev-notes>`.
:::

## Use in your own projects

The project is yet to be published on PyPI, so to install this project as a dependency,

```bash
uv add git+https://github.com/mardi4nfdi/morwiki.git
```
> If using `pip`, you can install it via,
> ```
> pip install git+https://github.com/mardi4nfdi/morwiki.git
> ```

You can then use it in your code,
```python
from morwiki import Database, Example

# List all example identifiers in Database
database = Database()
ids = database.list_ids()

# Pull metadata using ID
id = "steelProfile_n1357m7q6"
example = Example(id, database)
metadata = example.meta # or also, database.lookup(id)

# Fetch system matrices from Zenodo or server
example.retrieve()
matrices = example.data
```

The database currently has a subset of the benchmarks in [MORWiki](https://modelreduction.org/morwiki), and it is best to list ids to check if they exist.

`MORWiki` supports flexible configuration through environment variables or a YAML configuration file. See the {ref}`configuration guide <id-configuration>` for more details.

## Run Demos
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
