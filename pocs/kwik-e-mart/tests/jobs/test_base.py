from unittest.mock import MagicMock

from pyspark.sql import DataFrame

from kwik_e_mart.config import Config
from kwik_e_mart.jobs.base import Job

CONFIG = Config(lake_path="/lake")


class DummyJob(Job):
    name = "layer/dummy"

    def run(self) -> DataFrame:
        return MagicMock()


class ClusteredJob(DummyJob):
    cluster_by = ["branch", "date"]


def test_output_path_is_lake_path_plus_job_name():
    job = DummyJob(MagicMock(), MagicMock(), CONFIG)
    assert job.output_path == "/lake/layer/dummy"


def test_cluster_by_defaults_to_no_columns():
    job = DummyJob(MagicMock(), MagicMock(), CONFIG)
    assert job.cluster_by == []


def test_cluster_by_can_be_overridden_by_the_job():
    job = ClusteredJob(MagicMock(), MagicMock(), CONFIG)
    assert job.cluster_by == ["branch", "date"]
