from kwik_e_mart.jobs import JOBS, Job


def test_registry_has_the_sales_job():
    assert "silver/sales" in JOBS


def test_registry_is_keyed_by_job_name():
    assert all(key == job.name for key, job in JOBS.items())


def test_registry_only_holds_jobs():
    assert all(issubclass(job, Job) for job in JOBS.values())
