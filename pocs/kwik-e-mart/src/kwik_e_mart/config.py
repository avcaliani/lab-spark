from argparse import Namespace
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(frozen=True)
class Config:
    lake_path: str
    run_id: str
    run_ts: datetime


def load_config(args: Namespace) -> Config:
    return Config(
        lake_path=args.lake_path,
        run_id=str(uuid4()),
        run_ts=datetime.now(UTC),
        # If I need new configs, that comes from env variables,
        # for example, I can add them here and pass them to
        # the job context.
    )
