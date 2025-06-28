from typing import Union
from pathlib import Path
from urllib.parse import urljoin
from rich import print
import pooch
import logging

from morb_fetch.utils import parse_human_size, loadmat
from morb_fetch.config import get_config
from morb_fetch.examples.database import Database, get_database
from morb_fetch.examples.datasets import DataSetType

logger = pooch.get_logger()
logger.setLevel(logging.ERROR)

class Example:
    """
    A class to represent an example.
    It contains the metadata and the data associated with the example.
    """

    def __init__(
        self,
        meta: Union[dict, str],
        database: Union[Database, None] = None,
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
        filefolder.mkdir(parents=True, exist_ok=True)
        threshold = _config.max_filesize

        filepath = filefolder / filename
        try:
            data = loadmat(filepath)
        except OSError:
            if threshold is None or (
                parse_human_size(filesize) <= parse_human_size(threshold)
            ):
                print(
                    f"Data file {str(filepath)} not found. Trying to fetch from zenodo/server..."
                )
                fileurl = self.meta["zenodoLink"]
                if not fileurl.strip():
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

            _data = loadmat(Path(filepath)) # Load MAT
            self.data = DataSetType.validate_python(_data) # Validate and categorize dataset

        print(f"Loaded example data from {filepath}")

    def __getitem__(self, key):
        """
        Retrieve a value either from the metadata or data dictionary.
        This feature is added as syntactic sugar to make accessing metadata and data more convenient.

        Parameters
        ----------
        key : str
            The key to retrieve.

        Returns
        -------
        value : Any
            The value associated with the key.

        Raises
        ------
        KeyError
            If the key is not found in the metadata or data dictionary.
        """
        try:
            return self.meta[key]
        except KeyError:
            try:
                return getattr(self.data, key)
            except AttributeError:
                raise AttributeError(
                    f"'{self.__class__.__name__}' object has no 'data' attribute."
                    f" If you are trying to access matrices, first load the datasets using {self.__class__.__name__}.retrieve()"
                )
            except KeyError:
                raise KeyError(
                    f"'{self.__class__.__name__}' object has no '{key}' attribute."
                )
