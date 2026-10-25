from pyspark.sql import SparkSession


class SparkLogger:

    def __init__(self, spark: SparkSession, app_name: str, job_name: str) -> None:
        log4j = spark.sparkContext._jvm.org.apache.logging.log4j
        self.logger = log4j.LogManager.getLogger(app_name)
        self.job_name = job_name

    def info(self, msg: str) -> None:
        self.logger.info(f'[{self.job_name}] {msg}')

    def error(self, msg: str) -> None:
        self.logger.error(f'[{self.job_name}] {msg}')
