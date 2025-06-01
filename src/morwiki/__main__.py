import argparse
from pathlib import Path
from platformdirs import user_config_dir
from rich import print

parser = argparse.ArgumentParser(
    prog="morwiki",
    description="Creates a configuration file `morwiki.config.yaml` for MORWiki",
    epilog="You may edit the configuration file once it has been created",
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    "--create-config",
    nargs="?",
    const=".",
    metavar="CONFIG_DIR",
    help=(
        "Create a config file in the specified directory.\n"
        "  --create-config             → create in current directory\n"
        "  --create-config /some/path  → create in /some/path\n"
        "  --create-config user        → create in user config dir\n"
    ),
)
args = parser.parse_args()

if args.create_config is not None:
    if args.create_config == "user":
        config_dir = Path(
            user_config_dir(
                appname="morwiki", appauthor="morb-users", ensure_exists=True
            )
        )
    else:
        config_dir = Path(args.create_config).expanduser().resolve()

    config_data = """# Server configuration for MORWiki
    # Server URL, database file and file hash
    serverurl: "https://csc.mpi-magdeburg.mpg.de/mpcsc/MORB-data/"
    indexfile: "examples.csv"
    indexfilehash: "sha256:960a243420e3e2d229bebb26313541841c6d5b51b9f215d7ca7b77c6b3636791"

    # Custom Cache location : (by default it is the OS-specific user cache directory)
    # cache_dir: "~/.cache/morwiki"
    """

    yaml_path = config_dir / "morwiki.config.yaml"
    with open(yaml_path, "w") as f:
        f.write(config_data)

    print(f"Creating config in: {config_dir}")
