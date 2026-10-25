import sys
import traceback

from pyspark.sql import SparkSession
from src.kwik_e_mart import cli, config
from src.kwik_e_mart.infra import SparkLogger
from src.kwik_e_mart.jobs import JOBS

APP_NAME = "kwik-e-mart"

def init_spark() -> SparkSession:
    """Build the Spark session. Options are focused on running locally."""
    return (
        SparkSession.builder.appName(APP_NAME)
            .config("spark.sql.shuffle.partitions", "4")
            .config("spark.default.parallelism", "4")
            .config("spark.sql.session.timeZone", "UTC")
            .config("spark.driver.bindAddress", "127.0.0.1")
            .config("spark.driver.host", "127.0.0.1")
            .getOrCreate()
    )


def main() -> None:
    """Main entrypoint for the application."""
    args = cli.args()
    spark = init_spark()
    logger = SparkLogger(spark, APP_NAME, args.job_name)
    try:
        logger.info(f"Spark Version: {spark.version}")
        job_instance = JOBS[args.job_name](
            spark, 
            logger, 
            config.load_config(args)
        )
        output = job_instance.run()
        (job_instance
            .write_results(output)
            .show_results())

    except Exception as ex:
        logger.error(f"Unexpected Error! {ex}\n{traceback.format_exc()}")
        sys.exit(1)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
