import argparse
from pathlib import Path
from platformdirs import user_config_dir
from rich import print

parser = argparse.ArgumentParser(
    prog="morb_fetch",
    description="Configuration file management for MORB-fetch",
    epilog="You may edit the configuration file once it has been created, list available ones or delete them.",
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    "-c",
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

parser.add_argument(
    "-p",
    "--print-config",
    action="store_true",
    help="Print the configuration that morb-fetch uses",
)

parser.add_argument(
    "-l",
    "--list-config",
    action="store_true",
    help="List the configurations that morb-fetch finds",
)

parser.add_argument(
    "-d",
    "--delete-config",
    nargs="?",
    metavar="CONFIG_YAML",
    help=(
        "Delete a config file.\n"
        "  --delete-config /some/path/morb-fetch.config.yaml\n"
        "Delete all found config files\n"
        "  --delete-config all\n"
    ),
)

args = parser.parse_args()

if args.create_config is not None:
    from morb_fetch.config import create_config

    if args.create_config == "user":
        config_dir = Path(
            user_config_dir(
                appname="morb", appauthor="morb-users", ensure_exists=True
            )
        )
    else:
        config_dir = Path(args.create_config).expanduser().resolve()

    print(f"Creating config in: {config_dir}")
    yaml_path = config_dir / "morb_fetch.config.yaml"

    create_config(yaml_path)

if args.print_config:
    from morb_fetch.config import print_config

    print_config()

if args.list_config:
    from morb_fetch.config import list_config

    list_config()

if args.delete_config is not None:
    from pydantic import TypeAdapter
    from morb_fetch.config import list_config, delete_config, ConfigFilename

    if args.delete_config=="all":
        yaml_paths = list_config()
        for yaml_path in yaml_paths:
            print(f"Deleting config: {yaml_path}")
            delete_config(yaml_path)
    else:
        assert TypeAdapter(ConfigFilename).validate_python(args.delete_config)
        yaml_path = Path(args.delete_config).expanduser().resolve()
        print(f"Deleting config: {yaml_path}")
        delete_config(yaml_path)
