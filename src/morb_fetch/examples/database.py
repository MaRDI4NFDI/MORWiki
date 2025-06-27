from typing import Optional
from urllib.parse import urljoin
import polars as pl
import pooch
from rich import print
import logging

from morb_fetch.config import Settings, get_config

logger = pooch.get_logger()
logger.setLevel(logging.ERROR)

class Database:
    """
    A class to represent the examples database.
    It loads the examples from a CSV file and provides a method to fetch
    a specific example by name and identifier.
    """

    def __init__(self, config: Optional[Settings] = None):
        """
        Load the examples from the database.

        Args:
            config (Settings, optional): The configuration settings. Defaults to None.
        """
        if config is None:
            config = get_config()

        # Cache directory for downloaded files
        self.cache_dir = (config.cache).expanduser().resolve(strict=False) / "data"
        ## Create directory if it doesn't exist
        if not self.cache_dir.exists():
            print(f"Creating examples cache directory: {self.cache_dir}")
            self.cache_dir.mkdir(parents=True)

        # Path to the examples database
        fileurl = urljoin(str(config.serverurl), config.indexfile)
        self.filepath = self.cache_dir / config.indexfile
        try:
            # Check if the file is readable as a CSV
            self.data = pl.read_csv(
                self.filepath, infer_schema=False, missing_utf8_is_empty_string=True
            )
        except FileNotFoundError:
            print(
                f"Database {self.filepath} not found. Trying to fetch from server..."
            )
            self.filepath = pooch.retrieve(
                url=fileurl,
                known_hash=config.indexfilehash,
                path=self.cache_dir,
                fname=config.indexfile,
                progressbar=True,
            )
            self.data = pl.read_csv(
                self.filepath, infer_schema=False, missing_utf8_is_empty_string=True
            )
        print(
            f"[italic orange1]Loaded example database:[/italic orange1] {str(self.filepath)}"
        )

    def list_ids(self):
        """
        List all example identifiers.

        Returns:
            list[str]: The list of example identifiers.
        """
        return self.data["id"].to_list()

    def lookup(self, id: str) -> dict:
        """
        Lookup an example by its identifier.

        Args:
            id (str): The identifier of the example.

        Returns:
            dict: The example data.
        """
        example = self.data.filter(pl.col("id") == id)
        print(f"Lookup ID [yellow]{id}[/yellow]: ", end="")
        if example.is_empty():
            raise ValueError("not found!")
        else:
            print("found.")
            return example.to_dicts()[0]


# Singleton pattern for global access
_database: Database | None = None
_config: Settings | None = None

def get_database() -> Database:
    """
    Get the global database instance.

    Returns:
        Database: The global database instance.
    """
    global _database, _config
    if _config is None:
        _config = get_config()
    if _database is None:
        _database = Database(_config)

    return _database
