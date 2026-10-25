from argparse import Namespace
from dataclasses import FrozenInstanceError

import pytest

from kwik_e_mart.config import Config, load_config


def test_load_config_maps_the_cli_args():
    assert load_config(Namespace(lake_path="/lake")) == Config(lake_path="/lake")


def test_config_is_immutable():
    config = Config(lake_path="/lake")
    with pytest.raises(FrozenInstanceError):
        config.lake_path = "/other"
