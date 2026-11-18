package br.avcaliani.kwikechain

import br.avcaliani.kwikechain.pipelines.registry
import br.avcaliani.kwikechain.utils.{ArgParse, Properties}
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.slf4j.LoggerFactory

object Main extends App with Properties {

  private val log = LoggerFactory.getLogger(getClass)

  private val name = ArgParse.pipelineName(args)
  private val newPipeline = registry.getOrElse(
    name,
    throw new IllegalArgumentException(
      s"Unknown pipeline '$name'. Available pipelines: ${registry.keys.mkString(", ")}"
    )
  )
  private val appName = getProperty("app.name")
  // Master comes from spark-submit / spark-defaults.conf, don't hardcode it here
  private val spark = SparkSession
    .builder()
    .config(new SparkConf().setAppName(appName))
    .getOrCreate()

  log.debug(s"Running pipeline '$name'...")
  newPipeline(spark).run()

}
