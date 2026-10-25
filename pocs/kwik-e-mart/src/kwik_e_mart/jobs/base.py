from abc import ABC, abstractmethod
from textwrap import dedent
from typing import Self

from pyspark.sql import DataFrame, SparkSession
from src.kwik_e_mart.config import Config
from src.kwik_e_mart.infra import fs
from src.kwik_e_mart.infra.logging import SparkLogger


class Job(ABC):

    def __init__(self, spark: SparkSession, logger: SparkLogger, config: Config):
        self.spark = spark
        self.logger = logger
        self.config = config
        self.logger.info(f"Job started with config: {self.config}")

    # --- Common Properties ------------------------

    @property
    @abstractmethod
    def name(self) -> str:
        """unique name of the job. Used to identify the job in the CLI."""
        ...

    @property
    def output_path(self) -> str:
        """Path to write the output of the job to."""
        return f"{self.config.lake_path}/{self.name}"

    @property
    def cluster_by(self) -> list[str]:
        """Columns to cluster delta files by. Defaults to none."""
        return []

    # --- Common Methods ---------------------------

    @abstractmethod
    def run(self) -> DataFrame:
        """Main logic of the job. Must return final DataFrame."""
        ...

    def write_results(self, df: DataFrame) -> Self:
        self.logger.info(f"Writing results to {self.output_path}...")
        fs.write_delta(
            self.spark,
            df,
            self.output_path,
            self.cluster_by
        )
        return self

    def show_results(self) -> Self:
        results_summary = dedent("""\
        Job Results 👇
        Output Path: {path}
        Output Row Count: {count:,}
        Schema:
        {schema}""")

        df = fs.read_delta(self.spark, self.output_path)
        self.logger.info(
            results_summary.format(
                path=self.output_path,
                count=df.count(),
                schema=df.schema.treeString(),
            )
        )
        df.show(5)
        return self
