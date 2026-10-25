from unittest.mock import MagicMock

from kwik_e_mart.infra import SparkLogger


def build_logger():
    spark = MagicMock()
    log4j = spark.sparkContext._jvm.org.apache.logging.log4j
    return SparkLogger(spark, "app", "layer/job"), log4j.LogManager.getLogger


def test_logger_is_named_after_the_app():
    _, get_logger = build_logger()
    get_logger.assert_called_once_with("app")


def test_info_prefixes_the_job_name():
    logger, get_logger = build_logger()
    logger.info("hello")
    get_logger.return_value.info.assert_called_once_with("[layer/job] hello")


def test_error_prefixes_the_job_name():
    logger, get_logger = build_logger()
    logger.error("boom")
    get_logger.return_value.error.assert_called_once_with("[layer/job] boom")
