import pooch
from typing import Annotated, Optional
from typing_extensions import Doc
from pydantic import StringConstraints

from morb_fetch.config import get_config, Settings

logger = pooch.get_logger()
logger.setLevel("WARNING")

DOIstr = Annotated[
    str,
    StringConstraints(pattern=r"^doi:10\.\d{4,9}/[-._;()/:A-Z0-9]+$"),
    Doc(
        "A string starting with 'doi:' followed by record id."
    )
]
""" DOIstr: A string starting with 'doi:' followed by record id. """


class MORLABDownloader:
    """
    A class to download MORLAB releases from Zenodo
    """

    _registry: dict[str, DOIstr] = {
        "6.0": "doi:10.5281/zenodo.7072831",
        "5.0": "doi:10.5281/zenodo.3332716",
        "4.0": "doi:10.5281/zenodo.1574083",
        "3.0": "doi:10.5281/zenodo.842659",
    }

    @classmethod
    def list_available_versions(cls) -> list[str]:
        """
        List all available versions of MORLAB
        """
        return list(cls._registry.keys())

    @classmethod
    def retrieve_version(cls, version: str, config: Optional[Settings]=None) -> str:
        """
        Retrieve a specific version of MORLAB
        """
        # assert that version is valid
        available_versions = cls.list_available_versions()
        if version not in available_versions:
            raise ValueError(f"Version {version} not found. Available versions: {available_versions}")

        # metadata
        doi = cls._registry[version]
        zip_filename = f"morlab-{version}.zip"
        config = get_config()

        # build downloader from doi
        downloader = pooch.create(
            base_url=doi,
            path=config.cache / "morlab",
            registry=None,
        )
        downloader.load_registry_from_doi()

        # fetch file
        downloader.fetch(
            fname=zip_filename,
            processor=pooch.Unzip(extract_dir='.'),
            progressbar=True,
        )

        unzip_path = config.cache / "morlab" / f"morlab-{version}"
        print(f"MORLAB-{version} downloaded at {unzip_path}")

        return str(unzip_path)
