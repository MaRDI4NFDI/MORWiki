import polars as pl
import pooch
import typing
from rich import print
from urllib.parse import urljoin
from scipy.io import loadmat

from morwiki.config import Settings, get_config


class Database:
    """
    A class to represent the examples database.
    It loads the examples from a CSV file and provides a method to fetch
    a specific example by name and identifier.
    """

    def __init__(self, config: Settings = None):
        """
        Load the examples from the database.
        """
        if config is None:
            config = get_config()

        # Cache directory for downloaded files
        self.cache_dir = config.cache
        ## Create directory if it doesn't exist
        if not self.cache_dir.exists():
            print(f"Creating examples cache directory: {self.cache_dir}")
            self.cache_dir.mkdir(parents=True)

        # Path to the examples database
        fileurl = urljoin(str(config.serverurl), config.indexfile)
        self.filepath = pooch.retrieve(
            url=fileurl,
            known_hash=config.indexfilehash,
            path=self.cache_dir,
            fname=config.indexfile,
        )

        # Check if the file is readable as a CSV
        try:
            self.data = pl.read_csv(
                self.filepath,
                infer_schema=False,
                missing_utf8_is_empty_string=True
            )
            print(f"[italic orange1]Example database:[/italic orange1] {self.filepath}")
        except Exception as e:
            raise RuntimeError(f"Error loading data: {e}")

    def lookup(self, id:str) -> dict:
        """
        Lookup an example by its identifier.

        Args:
            id (str): The identifier of the example.

        Returns:
            dict: The example data.
        """
        example = self.data.filter(pl.col("id") == id)
        if example.is_empty():
            raise ValueError(f"ID {id} not found.")
        else:
            print(f"ID [yellow]{id}[/yellow] found.")
            return example.to_dicts()[0]

# Singleton pattern for global access
_database: Database | None = None
_config : Settings | None = None

def fetch_example_meta(id)-> dict:
    """
    Fetch metadata of example from the example database.

    Args:
        id (str): The identifier of the example.

    Returns:
        example: dict with ex ample metadata.
    """
    global _database, _config
    if _config is None:
        _config = get_config()
    if _database is None:
        _database = Database(_config)

    return _database.lookup(id)

def get_database():
    global _database, _config
    if _config is None:
        _config = get_config()
    if _database is None:
        _database = Database(_config)

    return _database

class Example:
    """
    A class to represent an example.
    It contains the metadata and the data associated with the example.
    """

    def __init__(self, meta:typing.Union[dict,str], database: typing.Union[Database, None]=None):
        """
        Initialize the example with metadata.

        Args:
            meta (dict): The metadata of the example.
        """
        self._database = database or get_database()
        if isinstance(meta, str):
            self.meta = fetch_example_meta(meta)
        elif isinstance(meta, dict):
            self.meta = meta
        else:
            raise ValueError("Argument must be an example id string or metadata dict.")

    def retrieve_matrices(self):
        self.file = self.meta['id'] + '.mat'
        _config = get_config()
        fileurl = urljoin(
            str(_config.serverurl),
            self.meta['category'] + '/' + self.file
        )
        self.filepath = pooch.retrieve(
            url = fileurl,
            known_hash = self.meta['sourceFilehash'],
            path = self._database.cache_dir / self.meta['category'],
            fname = self.file
        )
        try:
            self.data = loadmat(self.filepath)
            print(f"Loaded example data from {self.filepath}")
        except Exception as e:
            raise RuntimeError(f"Error loading .mat data: {e}")
