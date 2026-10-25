from datetime import datetime

from pyspark.sql import DataFrame
from pyspark.sql import functions as f

from kwik_e_mart.infra import fs
from kwik_e_mart.jobs.base import Job


class SalesJob(Job):

    # Output Path is defined based on the Job Name
    name = "silver/sales"
    cluster_by = ["branch", "date"]

    def run(self) -> DataFrame:
        df = fs.read_csv(
            spark = self.spark,
            path = f"{self.config.lake_path}/bronze/sales"
        )
        self.logger.info(f"Input Row Count: {df.count():,}")
        return (
            df.transform(self.rename_cols)
                .transform(self.parse_cols)
                .transform(self.data_quality)
                .transform(self.add_metadata, self.config.run_id, self.config.run_ts)
        )

    @staticmethod
    def rename_cols(df: DataFrame) -> DataFrame:
        new_names = map(
            lambda c: f.col(c).alias(str(c).strip().replace(" ", "_").lower()),
            df.columns,
        )
        return df.select(*list(new_names))

    @staticmethod
    def parse_cols(sales: DataFrame) -> DataFrame:
        unit_price = f.regexp_replace(f.col("unit_price"), r"\$", "")
        return (
            sales
                .withColumn("date", f.try_to_date(f.col("date"), "MMMM d, yyyy"))
                .withColumn("quantity", f.col("quantity").cast("long"))
                .withColumn("unit_price", unit_price.cast("double"))
                .withColumn("discount_pct", f.col("discount_pct").cast("double"))
        )

    @staticmethod
    def data_quality(sales: DataFrame) -> DataFrame:
        return sales.withColumn(
            "is_valid",
            ~f.col("salesperson").isNull()
                & ~f.col("date").isNull()
                & (f.col("quantity") >= 0),
        )

    @staticmethod
    def add_metadata(sales: DataFrame, run_id: str, run_ts: datetime) -> DataFrame:
        return (
            sales
                .withColumn("run_id", f.lit(run_id))
                .withColumn("run_ts", f.lit(run_ts))
        )
