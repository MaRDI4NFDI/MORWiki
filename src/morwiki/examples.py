import polars as pl
import pooch
import typing
from rich import print
from urllib.parse import urljoin
from scipy.io import loadmat

from morwiki.config import Settings, get_config, HumanFileSize


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
        self.cache_dir = (config.cache).expanduser().resolve(strict=False)
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

def get_database()-> Database:
    global _database, _config
    if _config is None:
        _config = get_config()
    if _database is None:
        _database = Database(_config)

    return _database


def _parse_human_size(s:HumanFileSize)-> int:
    units = {
        "B": 1, "KB": 10**3, "MB": 10**6, "GB": 10**9,
        "KIB": 2**10, "MIB": 2**20, "GIB": 2**30
    }
    s = s.strip().upper().replace(" ", "")
    for unit in sorted(units.keys(), key=len, reverse=True):
        if s.endswith(unit):
            num = float(s[:-len(unit)])
            return int(num * units[unit])
    
    raise ValueError(f"Could not parse size: {s}")

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
        _config = get_config()
        filename = self.meta['id'] + '.mat'
        filesize = self.meta['sourceFilesize']
        filefolder = self._database.cache_dir / self.meta['category']
        threshold = _config.max_filesize

        try:
            filepath = filefolder / filename
            data = loadmat(filepath)
        except OSError:
            print(f"Data file not found in {filepath}. Trying to fetch from server...")
            if threshold is None or (_parse_human_size(filesize) <= _parse_human_size(threshold)):
                fileurl = urljoin(
                    str(_config.serverurl),
                    self.meta['category'] + '/' + filename
                )
                filepath = pooch.retrieve(
                    url = fileurl,
                    known_hash = self.meta['sourceFilehash'],
                    path = filefolder,
                    fname = filename,
                    progressbar=True
                )
            else:
                raise ValueError(f"File size {filesize} exceeds allowed threshold of {threshold}.")
            data = loadmat(filepath)

        print(f"Loaded example data from {filepath}")
        self.filepath, self.data = filepath, data
