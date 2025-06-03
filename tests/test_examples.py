import os
import polars as pl
from morwiki.config import get_config
from morwiki.examples import Database, fetch_example_meta, Example


def test_database():
    config = get_config()
    db = Database(config)
    # check if indexfile is retrieved
    # hash is already verified by pooch during runtime
    assert os.path.basename(db.filepath) == config.indexfile

    # check if data is loaded
    assert db.data is not None
    assert isinstance(db.data, pl.DataFrame)

    # check data veracity and lookup is possible
    # TODO: width can be flexible and need not be a fixed value
    assert db.data.width == 50
    assert db.data["id"].shape[0] > 0


def test_fetch_example_meta():
    config = get_config()
    db = Database(config)

    sample_meta = fetch_example_meta(db.data["id"][0])
    assert set(sample_meta.keys()) == set(db.data.columns)


def test_example_initialization():
    config = get_config()
    db = Database(config)

    # initialize with id
    sample_example_1 = Example(db.data["id"][0])

    # initialize with meta
    sample_meta = fetch_example_meta(db.data["id"][0])
    sample_example_2 = Example(sample_meta)

    assert sample_example_1.meta == sample_example_2.meta


def test_example_matrices():
    pass
