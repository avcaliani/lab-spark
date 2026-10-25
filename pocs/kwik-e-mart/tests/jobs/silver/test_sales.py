import csv
from datetime import UTC, date, datetime
from unittest.mock import MagicMock

from pyspark.sql import functions as f
from pyspark.sql.types import BooleanType, DateType, DoubleType, LongType, StringType, StructField, StructType
from pyspark.testing.utils import assertDataFrameEqual

from kwik_e_mart.config import Config
from kwik_e_mart.jobs.silver.sales import SalesJob

COLUMNS = ["sale_id", "date", "branch", "salesperson", "client", "product", "quantity", "unit_price", "discount_pct"]

# Schema for rows already in parse_cols' output shape.
# Typed, so a lone None in a single-row DataFrame doesn't defeat Spark's 
# type inference
PARSED_SCHEMA = StructType([
    StructField("sale_id", StringType()),
    StructField("date", DateType()),
    StructField("branch", StringType()),
    StructField("salesperson", StringType()),
    StructField("client", StringType()),
    StructField("product", StringType()),
    StructField("quantity", LongType()),
    StructField("unit_price", DoubleType()),
    StructField("discount_pct", DoubleType()),
])
VALIDATED_SCHEMA = StructType([*PARSED_SCHEMA.fields, StructField("is_valid", BooleanType())])

RUN_ID = "5d1c0f0e-0d52-4b63-9a53-0a9f3f0e7c11"
RUN_TS = datetime(2026, 10, 25, 1, 2, 3, tzinfo=UTC)


def test_rename_cols(spark):
    df = spark.createDataFrame(
        [("1", "January 5, 2024", "Springfield", "Apu", "Homer Simpson", "Buzz Cola", "10", "$12.50", "5")],
        ["Sale Id", " DATE ", "Branch", "Salesperson", "Client", "Product", "Quantity", "Unit Price", "Discount Pct"],
    )
    result = SalesJob.rename_cols(df)
    assert result.columns == COLUMNS


def test_parse_cols(spark):
    df = spark.createDataFrame([
        # clean row
        ("1", "January 5, 2024", "Springfield", "Apu", "Homer Simpson", "Buzz Cola", "10", "$12.50", "5"),
        # missing date parses to null instead of raising under ANSI mode
        ("2", "", "Springfield", "Manjula", "Homer Simpson", "Duff Beer", "-3", "$99.99", "0"),
        # date in an unexpected format parses to null
        ("3", "2024-01-05", "Springfield", "Apu", "Homer Simpson", "Buzz Cola", "10", "$12.50", "5"),
    ], COLUMNS)
    expected = spark.createDataFrame([
        ("1", date(2024, 1, 5), "Springfield", "Apu", "Homer Simpson", "Buzz Cola", 10, 12.50, 5.0),
        ("2", None, "Springfield", "Manjula", "Homer Simpson", "Duff Beer", -3, 99.99, 0.0),
        ("3", None, "Springfield", "Apu", "Homer Simpson", "Buzz Cola", 10, 12.50, 5.0),
    ], PARSED_SCHEMA)
    assertDataFrameEqual(SalesJob.parse_cols(df), expected)


def test_data_quality(spark):
    expected = spark.createDataFrame([
        # clean row
        ("1", date(2024, 1, 5), "Springfield", "Apu", "Homer Simpson", "Buzz Cola", 10, 12.50, 5.0, True),
        # missing date
        ("2", None, "Springfield", "Manjula", "Homer Simpson", "Duff Beer", 5, 99.99, 0.0, False),
        # missing salesperson
        ("3", date(2024, 1, 6), "Springfield", None, "Homer Simpson", "Squishee", 2, 5.00, 0.0, False),
        # negative quantity (returns)
        ("4", date(2024, 1, 7), "Springfield", "Sanjay", "Homer Simpson", "Pink Donuts", -3, 3.00, 0.0, False),
        # zero quantity is the boundary and stays valid
        ("5", date(2024, 1, 8), "Springfield", "Sanjay", "Homer Simpson", "Pink Donuts", 0, 3.00, 0.0, True),
    ], VALIDATED_SCHEMA)
    assertDataFrameEqual(
        SalesJob.data_quality(expected.drop("is_valid")), 
        expected
    )


def test_add_metadata(spark):
    df = spark.createDataFrame([("1",), ("2",)], ["sale_id"])

    result = SalesJob.add_metadata(df, RUN_ID, RUN_TS)

    assert result.columns == ["sale_id", "run_id", "run_ts"]
    assert dict(result.dtypes)["run_ts"] == "timestamp"
    assert {row.run_id for row in result.collect()} == {RUN_ID}
    epochs = {row.epoch for row in result.select(f.unix_timestamp("run_ts").alias("epoch")).collect()}
    assert epochs == {int(RUN_TS.timestamp())}


def test_run_end_to_end(spark, tmp_path):
    bronze = tmp_path / "bronze" / "sales"
    bronze.mkdir(parents=True)
    with (bronze / "part-00000.csv").open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(COLUMNS)
        writer.writerows([
            ("1", "January 5, 2024", "Springfield", "Apu", "Homer Simpson", "Buzz Cola", 10, "$12.50", 5),
            ("2", "January 6, 2024", "Springfield", "", "Homer Simpson", "Squishee", 2, "$5.00", 0),
            ("3", "", "Shelbyville", "Manjula", "Marge Simpson", "Duff Beer", 5, "$99.99", 10),
            ("4", "January 7, 2024", "Shelbyville", "Sanjay", "Bart Simpson", "Chili Dog", -3, "$3.00", 0),
        ])

    job = SalesJob(spark, MagicMock(), Config(lake_path=str(tmp_path), run_id=RUN_ID, run_ts=RUN_TS))
    result = job.run()

    assert result.columns == [*COLUMNS, "is_valid", "run_id", "run_ts"]
    assert dict(result.dtypes) == {
        "sale_id": "string",
        "date": "date",
        "branch": "string",
        "salesperson": "string",
        "client": "string",
        "product": "string",
        "quantity": "bigint",
        "unit_price": "double",
        "discount_pct": "double",
        "is_valid": "boolean",
        "run_id": "string",
        "run_ts": "timestamp",
    }
    assert {row.run_id for row in result.collect()} == {RUN_ID}
    assert {row.sale_id: row.is_valid for row in result.collect()} == {
        "1": True,
        "2": False,
        "3": False,
        "4": False,
    }
