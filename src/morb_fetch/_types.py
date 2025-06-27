from typing import Annotated
from typing_extensions import Doc
from pydantic import StringConstraints

# Custom annotated types
SHA256Hash = Annotated[
    str,
    StringConstraints(pattern=r"^sha256:[a-fA-F0-9]{64}$"),
    Doc(
        "A string starting with 'sha256:' followed by a 64-character hexadecimal hash."
    ),
]
"""SHA256Hash: A SHA-256 hash string prefixed with 'sha256:'"""

CSVFilename = Annotated[
    str, StringConstraints(pattern=r".+\.csv$"), Doc("A filename ending in '.csv'.")
]
"""CSVFilename: A filename ending in '.csv'"""

ConfigFilename = Annotated[
    str,
    StringConstraints(pattern=r".+\.yaml$"),
    Doc("A filename ending in '.yaml'."),
]
"""ConfigFilename: A filename ending in '.yaml'"""

HumanFileSize = Annotated[
    str,
    StringConstraints(
        pattern=r"(?i)^\s*[0-9]+(\.[0-9]+)?\s*(B|KB|MB|GB|TB|KIB|MIB|GIB|TIB)\s*$"
    ),
    Doc("A human-readable file size like '10 MB' or '1.5 GiB'."),
]

"""HumanFileSize: A human-readable file size like '10 MB' or '1.5 GiB'."""

DOIstr = Annotated[
    str,
    StringConstraints(pattern=r"^doi:10\.\d{4,9}/[-._;()/:A-Z0-9]+$"),
    Doc(
        "A string starting with 'doi:' followed by record id."
    )
]
""" DOIstr: A string starting with 'doi:' followed by record id. """
