from pyspark.testing.utils import assertDataFrameEqual

from kwik_e_mart.infra import fs


def test_read_csv_uses_the_header_and_keeps_everything_as_string(spark, tmp_path):
    (tmp_path / "part-00000.csv").write_text("id,branch\n1,Springfield\n2,Shelbyville\n")

    df = fs.read_csv(spark, str(tmp_path))

    assert dict(df.dtypes) == {"id": "string", "branch": "string"}
    assert df.count() == 2


def test_write_delta_then_read_delta_returns_the_same_rows(spark, tmp_path):
    df = spark.createDataFrame([("1", "Springfield"), ("2", "Shelbyville")], ["id", "branch"])
    path = str(tmp_path / "out")

    fs.write_delta(spark, df, path, ["branch"])

    assertDataFrameEqual(fs.read_delta(spark, path), df)


def test_write_delta_replaces_the_rows_of_an_existing_table(spark, tmp_path):
    first = spark.createDataFrame([("1", "Springfield")], ["id", "branch"])
    second = spark.createDataFrame([("2", "Shelbyville"), ("3", "Ogdenville")], ["id", "branch"])
    path = str(tmp_path / "out")

    fs.write_delta(spark, first, path, ["branch"])
    fs.write_delta(spark, second, path, ["branch"])

    assertDataFrameEqual(fs.read_delta(spark, path), second)


def test_write_delta_adds_new_columns_to_an_existing_table(spark, tmp_path):
    first = spark.createDataFrame([("1", "Springfield")], ["id", "branch"])
    second = spark.createDataFrame([("2", "Shelbyville", "run-1")], ["id", "branch", "run_id"])
    path = str(tmp_path / "out")

    fs.write_delta(spark, first, path, ["branch"])
    fs.write_delta(spark, second, path, ["branch"])

    assertDataFrameEqual(fs.read_delta(spark, path), second)
