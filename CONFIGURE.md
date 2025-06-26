# MORWiki Configuration

<!-- SPHINX-START -->
`MORWiki` supports flexible configuration through environment variables or a YAML configuration file.

The precedence for configuration values is as follows (from highest to lowest):
1. environment variables,
2. configuration file (YAML),
3. default configuration.

The active configuration can either be inspected through the command line interface(CLI) by,
```bash
uv run python3 -m morwiki --print-config
```
or, within a Python script as,
```python
from morwiki import print_config
print_config()
```

## Default Configuration

The default configuration is as follows:

| Property | Value |
| ---------------|-----------|
| Server URL     | `https://modelreduction.org/morb-data/` |
| Indexfile      | `examples.csv` |
| Indexfile hash | `sha256:960a243420e3e2d229bebb26313541841c6d5b51b9f215d7ca7b77c6b3636791` |
| Max Filesize   | `None` |
| Cache Location | OS-specific cache path (e.g. `~/.cache/morwiki` on Linux) |

This configuration is overridden either by setting environment variables or a configuration file.

## Environment Variables

The following environment variables correspond to the configuration properties:

- `MORWIKI_SERVERURL`: The base URL for the MorWiki server.
- `MORWIKI_INDEXFILE`: The filename of the index file.
- `MORWIKI_INDEXFILEHASH`: The SHA256 hash of the index file.
- `MORWIKI_MAX_FILESIZE`: The maximum file size allowed for download.
- `MORWIKI_CACHE`: The path to the cache directory.

For example, to restrict the maximum file size to 100MB, in the bash prompt this can be done with,

```bash
export MORWIKI_MAX_FILESIZE=100MB
```

Follow your operating system's instructions to set environment variables.

## Configuration File

In addition to environment variables, configuration can be provided via a YAML file named `morwiki.config.yaml`.
To generate a template configuration file at a specific path (e.g. `/some/path`), run:

```bash
uv run python3 -m morwiki --create-config /some/path
```
If no path is specified, the configuration file will be created in the current working directory.
Using the `--create-config user` option places the file in the user's config directory (`~/.config/morwiki` on Linux).

To specify a custom configuration file located elsewhere, set the `MORWIKI_CONFIG_FILE` environment variable:
```bash
export MORWIKI_CONFIG_FILE=/path/to/config.yaml
```
The precedence of configuration file lookup is as follows:
1. `MORWIKI_CONFIG_FILE` value
2. `morwiki.config.yaml` in the current working directory
3. `morwiki.config.yaml` in the user's config directory (e.g. `~/.config/morwiki` on Linux)

### Managing configuration files

To list configuration files (found in above context), run:

```bash
uv run python3 -m morwiki --list-config
```

To delete a configuration file, run:

```bash
uv run python3 -m morwiki --delete-config /some/path/morwiki.config.yaml
```

To delete all found configuration files, run:

```bash
uv run python3 -m morwiki --delete-config all
```

> These management functions are useful for handling static configuration of MORWiki.
> For dynamic configuration, note that you would need to use `clear_config()`
> before re-initiating config with `get_config()`.
