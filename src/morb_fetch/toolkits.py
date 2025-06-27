import pooch
from typing import Annotated, ClassVar, Optional
from typing_extensions import Doc
from pydantic import BaseModel, StringConstraints

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


class ToolkitDownloader(BaseModel):
    """
    A class to download MORLAB releases from Zenodo
    """
    name: ClassVar[str]
    registry: ClassVar[dict[str, DOIstr]]

    @classmethod
    def list_available_versions(cls) -> list[str]:
        """
        List all available versions of MORLAB
        """
        return list(cls.registry.keys())

    @classmethod
    def retrieve_version(cls, version: str, config: Optional[Settings]=None) -> str:
        """
        Retrieve a specific version of Toolkit
        """
        # assert that version is valid
        available_versions = cls.list_available_versions()
        if version not in available_versions:
            raise ValueError(f"Version {version} not found. Available versions: {available_versions}")

        # metadata
        doi = cls.registry[version]
        zip_filename = f"{cls.name}-{version}.zip"
        config = get_config()

        # build downloader from doi
        downloader = pooch.create(
            base_url=doi,
            path=config.cache / cls.name,
            registry=None,
        )
        downloader.load_registry_from_doi()

        # fetch file
        downloader.fetch(
            fname=zip_filename,
            processor=pooch.Unzip(extract_dir='.'),
            progressbar=True,
        )

        unzip_path = config.cache / cls.name / f"{cls.name}-{version}"
        print(f"{cls.name}-{version} downloaded at {unzip_path}")

        return str(unzip_path)


class MORLABDownloader(ToolkitDownloader):
    name = "morlab"
    registry = {
        "6.0": "doi:10.5281/zenodo.7072831",
        "5.0": "doi:10.5281/zenodo.3332716",
        "4.0": "doi:10.5281/zenodo.1574083",
        "3.0": "doi:10.5281/zenodo.842659",
    }


class MMESSDownloader(ToolkitDownloader):
    name = "MMESS"
    registry = {
        "3.1": "doi:10.5281/zenodo.14929081",
        "3.0": "doi:10.5281/zenodo.7701424",
        "2.2": "doi:10.5281/zenodo.5938237",
        "2.1": "doi:10.5281/zenodo.4719688",
        "2.0.1": "doi:10.5281/zenodo.3606345",
        "2.0": "doi:10.5281/zenodo.3368844",
        "1.0.1": "doi:10.5281/zenodo.50575",
    }
