from argparse import Namespace
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    lake_path: str
    job_name: str


def load_config(args: Namespace) -> Config:
    return Config(
        lake_path=args.lake_path,
        job_name=args.job_name,
        # If I need new configs, that comes from env variables,
        # for example, I can add them here and pass them to
        # the job context.
    )
