import pytest

from kwik_e_mart import cli


def test_job_is_mapped_to_job_name(monkeypatch):
    monkeypatch.setattr("sys.argv", ["kwik-e-mart", "--job", "silver/sales"])
    assert cli.parse_args().job_name == "silver/sales"


def test_lake_path_has_a_default(monkeypatch):
    monkeypatch.setattr("sys.argv", ["kwik-e-mart", "-j", "silver/sales"])
    assert cli.parse_args().lake_path == "/data/kwik-e-mart"


def test_lake_path_can_be_overridden(monkeypatch):
    monkeypatch.setattr("sys.argv", ["kwik-e-mart", "-j", "silver/sales", "--lake-path", "/tmp/lake"])
    assert cli.parse_args().lake_path == "/tmp/lake"


def test_unknown_job_exits_with_usage_error(monkeypatch):
    monkeypatch.setattr("sys.argv", ["kwik-e-mart", "--job", "does/not-exist"])
    with pytest.raises(SystemExit) as exit_info:
        cli.parse_args()
    assert exit_info.value.code == 2


def test_job_is_required(monkeypatch):
    monkeypatch.setattr("sys.argv", ["kwik-e-mart"])
    with pytest.raises(SystemExit) as exit_info:
        cli.parse_args()
    assert exit_info.value.code == 2
