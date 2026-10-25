from src.kwik_e_mart.jobs import silver
from src.kwik_e_mart.jobs.base import Job

JOBS: dict[str, type[Job]] = {
    job.name: job for job in [
        silver.SalesJob
    ]
}

__all__ = ["Job", "JOBS"]
