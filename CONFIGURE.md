# MORWiki Configuration

`MORWiki` supports flexible configuration through environment variables or a YAML configuration file.
<!-- SPHINX-START -->
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

### Managing configuration files

To print the active configuration, run:

```bash
uv run python3 -m morwiki --print-config
```

To list configuration files (found in above context), run:

```bash
uv run python3 -m morwiki --list-configs
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
