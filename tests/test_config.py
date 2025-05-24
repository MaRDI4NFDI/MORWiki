import os
import pytest
from pathlib import Path
from morwiki.config import get_config, clear_config

@pytest.fixture
def mock_yaml_file(tmp_path):
    config_data = """
    serverurl: 'https://www.example.com/test_server/'
    indexfile: "test_examples.csv"
    indexfilehash: "sha256:268838a990c991a29efe3469952c196b37dae0ac98d62d847748ade5bfa6af1d"
    cache: "./.test_cache"
    """
    yaml_path = tmp_path / "morb.yaml"
    with open(yaml_path, "w") as f:
        f.write(config_data)
    return yaml_path

def test_load_default_config():
    """Test loading default config (using default file and env)"""
    # Clear any existing environment variable
    os.environ.pop("MORWIKI_CONFIG_FILE", None)

    # Load the config
    config = get_config()

    # Check default values
    assert config.cache == Path("./.cache")

    clear_config()


def test_load_yaml_config_from_env(monkeypatch, mock_yaml_file):
    """Test loading config from a YAML file"""
    # Set the config file environment variable
    monkeypatch.setenv("MORWIKI_CONFIG_FILE", str(mock_yaml_file))

    # Load the config
    config = get_config()

    # Assert the config values from YAML file
    assert config.cache == Path('./.test_cache')

    clear_config()
