from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter

from kwik_e_mart.jobs import JOBS

DESCRIPTION = """
\033[1;33m🏪 Kwik-E-Mart\033[0m
\033[36mThank you, come again!\033[0m

Run a Kwik-E-Mart PySpark Job.
"""


def parse_args() -> Namespace:
    parser = ArgumentParser(
        prog="kwik-e-mart",
        description=DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-j",
        "--job",
        dest="job_name",
        required=True,
        choices=sorted(JOBS.keys()),
        help="Name of the job to run.",
    )
    parser.add_argument(
        "--lake-path",
        default="/data/kwik-e-mart",
        help="Root path of the data lake.",
    )
    return parser.parse_args()
