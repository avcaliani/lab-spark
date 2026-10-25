from argparse import Namespace
from unittest.mock import MagicMock

import pytest

from kwik_e_mart import main as app


@pytest.fixture
def spark(monkeypatch):
    session = MagicMock()
    monkeypatch.setattr(app, "init_spark", lambda: session)
    monkeypatch.setattr(app.cli, "parse_args", lambda: Namespace(job_name="fake", lake_path="/lake"))
    return session


def test_main_runs_writes_and_shows_results_then_stops_spark(monkeypatch, spark):
    job_class = MagicMock()
    monkeypatch.setattr(app, "JOBS", {"fake": job_class})

    app.main()

    job = job_class.return_value
    job.run.assert_called_once()
    job.write_results.assert_called_once_with(job.run.return_value)
    job.write_results.return_value.show_results.assert_called_once()
    spark.stop.assert_called_once()


def test_main_exits_with_code_1_and_stops_spark_when_the_job_fails(monkeypatch, spark):
    job_class = MagicMock()
    job_class.return_value.run.side_effect = RuntimeError("boom")
    monkeypatch.setattr(app, "JOBS", {"fake": job_class})

    with pytest.raises(SystemExit) as exit_info:
        app.main()

    assert exit_info.value.code == 1
    spark.stop.assert_called_once()
