import os
from rich.console import Console
from rich.table import Table
from rich import print
from typing import Annotated
from pathlib import Path
from pydantic import AnyHttpUrl, StringConstraints
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource
)

# Custom annotated types for SHA256 hash and CSV filenames
SHA256Hash = Annotated[str, StringConstraints(pattern=r"^sha256:[a-fA-F0-9]{64}$")]
CSVFilename = Annotated[str, StringConstraints(pattern=r".+\.csv$")]

# Find path for defaults.yaml file
PROJECT_ROOT = Path(__file__).parent.parent.parent
DEFAULT_CONFIG_FILE = (PROJECT_ROOT / "defaults.yaml").resolve()

class Settings(BaseSettings):
    serverurl: AnyHttpUrl="https://csc.mpi-magdeburg.mpg.de/mpcsc/MORB-data/",
    indexfile: CSVFilename="examples.csv",
    indexfilehash: SHA256Hash="sha256:960a243420e3e2d229bebb26313541841c6d5b51b9f215d7ca7b77c6b3636791",
    cache: Path= Path('.cache/')

    # Pydantic Model config: to import the settings from environment variables
    model_config = SettingsConfigDict(
        env_prefix="morwiki_",
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        Customise the settings sources and priorities to include a YAML file and environment variable.

        Priority: Source file defaults < YAML File < Environment Variables
        """
        CONFIG_FILE = Path(os.getenv("MORWIKI_CONFIG_FILE", DEFAULT_CONFIG_FILE))

        if not CONFIG_FILE.exists():
            Warning(f"Could not find config at {CONFIG_FILE}. Using runtime defaults!")
            return (env_settings, init_settings)
        else:
            print(f"[italic orange1]Config:[/italic orange1] {CONFIG_FILE}")
            return (
                env_settings,
                YamlConfigSettingsSource(
                    settings_cls,
                    yaml_file=CONFIG_FILE
                ),
                init_settings
            )

# Singleton pattern for global access
_config: Settings | None = None

def get_config() -> Settings:
    """
    Get the global configuration for package
    """
    global _config
    if _config is None:
        _config = Settings()

    return _config

def clear_config():
    """
    Unset the global configuration for package
    """
    global _config
    _config = None

def print_config() -> None:
    """
    Print the current configuration.
    """

    def _print_dict_as_table(
            title:str,
            data:dict,
            colors=['magenta', 'deep_sky_blue1', 'orange1'],
            console=None,
        ):

        if console is None:
            console = Console()

        table = Table(
            title=title,
            show_header=False,
            box=None,
            title_justify='left',
            title_style=f'bold italic {colors[2]}'
        )

        table.add_column(style=f"{colors[0]}")
        table.add_column(style=f"{colors[1]}")

        for key, value in data.items():
            table.add_row(str(key), str(value))

        return console.print(table)

    _print_dict_as_table(
        title = 'MORWIKI Configuration',
        data=get_config().model_dump(),
        console=Console()
    )
