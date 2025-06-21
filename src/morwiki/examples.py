import polars as pl
import pooch
import typing
from rich import print
import logging
from urllib.parse import urljoin
from scipy.io import loadmat

from morwiki.config import Settings, get_config, HumanFileSize

logger = pooch.get_logger()
logger.setLevel(logging.ERROR)


class Database:
    """
    A class to represent the examples database.
    It loads the examples from a CSV file and provides a method to fetch
    a specific example by name and identifier.
    """

    def __init__(self, config: typing.Optional[Settings] = None):
        """
        Load the examples from the database.

        Args:
            config (Settings, optional): The configuration settings. Defaults to None.
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
            f"[italic orange1]Loaded example database:[/italic orange1] {self.filepath}"
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


def _parse_human_size(s: HumanFileSize) -> int:
    """
    Parse a human-readable size string into an integer.

    Args:
        s (HumanFileSize): The human-readable size string.

    Returns:
        int: The parsed size in bytes.

    Raises:
        ValueError: If the size string is invalid.
    """
    units = {
        "B": 1,
        "KB": 10**3,
        "MB": 10**6,
        "GB": 10**9,
        "KIB": 2**10,
        "MIB": 2**20,
        "GIB": 2**30,
    }
    s = s.strip().upper().replace(" ", "")
    for unit in sorted(units.keys(), key=len, reverse=True):
        if s.endswith(unit):
            num = float(s[: -len(unit)])
            return int(num * units[unit])

    raise ValueError(f"Could not parse size: {s}")


class Example:
    """
    A class to represent an example.
    It contains the metadata and the data associated with the example.
    """

    def __init__(
        self,
        meta: typing.Union[dict, str],
        database: typing.Union[Database, None] = None,
    ):
        """
        Lookup the example ID in `Database` and initialize with metadata.

        Args:
            meta (dict): The metadata of the example.
        """
        self._database = database or get_database()
        if isinstance(meta, str):
            self.meta = self._database.lookup(meta)
        elif isinstance(meta, dict):
            self.meta = meta
        else:
            raise ValueError("Argument must be an example id string or metadata dict.")

    def retrieve(self):
        """
        Retrieve the data associated with the example either from the local cache or from the server.

        Returns:
            None
        """
        _config = get_config()
        filename = self.meta["id"] + ".mat"
        filesize = self.meta["sourceFilesize"]
        filefolder = self._database.cache_dir / self.meta["category"]
        threshold = _config.max_filesize

        filepath = filefolder / filename
        try:
            data = loadmat(filepath)
        except OSError:
            if threshold is None or (
                _parse_human_size(filesize) <= _parse_human_size(threshold)
            ):
                print(
                    f"Data file {filepath} not found. Trying to fetch from zenodo/server..."
                )
                try:
                    fileurl = self.meta["zenodoLink"]
                except KeyError:
                    fileurl = urljoin(
                        str(_config.serverurl), self.meta["category"] + "/" + filename
                    )
                filepath = pooch.retrieve(
                    url=fileurl,
                    known_hash=self.meta["sourceFilehash"],
                    path=filefolder,
                    fname=filename,
                    progressbar=True,
                )
            else:
                raise ValueError(
                    f"File size {filesize} exceeds maximum download size of {threshold}."
                )
            data = loadmat(filepath)

        print(f"Loaded example data from {filepath}")
        self.filepath, self.data = filepath, data
