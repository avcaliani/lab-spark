package br.avcaliani.kwikechain.pipelines

import br.avcaliani.kwikechain.utils.FSUtil
import br.avcaliani.kwikechain.utils.Properties
import org.apache.spark.sql.functions.{broadcast, lit, not}
import org.apache.spark.sql.{Column, DataFrame, SparkSession}
import org.slf4j.LoggerFactory

/** Reads the DonutCoin (DONU) transaction ledger, validates it, and writes the success/error/debug outputs */
case class DailyTransactionsPipeline(spark: SparkSession) extends Pipeline with Properties {

  import spark.implicits._

  private val log         = LoggerFactory.getLogger(getClass)
  private val DATA_BRONZE = getProperty("data.bronze")
  private val DATA_SILVER = getProperty("data.silver")
  private val CLUSTER_BY  = Seq("from_user", "to_user")

  override def run(): Unit = {

    val fs = new FSUtil(spark)

    log.debug("Task::Read")
    val transactions = fs.read(s"$DATA_BRONZE/kwik_e_chain/transactions/donu")
      .select(
        $"transaction_id",
        $"timestamp",
        $"from_user",
        $"to_user",
        $"amount_cents".cast("long"),
        $"currency",
        $"fee_cents".cast("long")
      )
    log.info(f"Input count: ${transactions.count()}%,d")

    val users = fs.read(s"$DATA_BRONZE/springfield/users")
      .select($"user_name")

    log.debug("Task::Validate")
    val flaggedTxn = transactions
        .transform(validate(users))
        .cache() // Will be written 3 times

    log.debug("Task::Write")
    writeOutputs(fs, flaggedTxn)
  }

  private def writeOutputs(fs: FSUtil, transactions: DataFrame): Unit = {
    val dropColumns = transactions.columns.filter(_.endsWith("_valid"))
    val dfOk        = transactions.filter($"is_valid").drop(dropColumns: _*)
    val dfErr       = transactions.filter(not($"is_valid")).drop(dropColumns: _*)

    fs.writeDelta(s"$DATA_SILVER/kwik_e_chain/transactions/donu_debug", transactions, CLUSTER_BY)
    fs.writeDelta(s"$DATA_SILVER/kwik_e_chain/transactions/donu_error", dfErr, CLUSTER_BY)
    fs.writeDelta(s"$DATA_SILVER/kwik_e_chain/transactions/donu_success", dfOk, CLUSTER_BY)

    log.info(f"Debug count: ${transactions.count()}%,d")
    log.info(f"Error count: ${dfErr.count()}%,d")
    log.info(f"Success count: ${dfOk.count()}%,d")
    dfOk.printSchema()
    dfOk.show(5)
  }

  private def isPositiveAmount: Column = $"amount_cents" > 0

  private def isNotSelfTransfer: Column = $"from_user" =!= $"to_user"

  private def isFeeValid: Column = $"fee_cents" === ($"amount_cents" / lit(20)).cast("long")

  private def withKnownUserFlag(userCol: String, flagCol: String, knownUsers: DataFrame)(df: DataFrame): DataFrame = {
    val matchColumn = s"__${userCol}_match"
    df
      .join(knownUsers.withColumnRenamed("user_name", matchColumn), $"$userCol" === $"$matchColumn", "left")
      .withColumn(flagCol, $"$matchColumn".isNotNull)
      .drop(matchColumn)
  }

  def validate(users: DataFrame)(transactions: DataFrame): DataFrame = {
    val knownUsers = broadcast(users.select($"user_name"))

    transactions
      .withColumn("amount_valid", isPositiveAmount)
      .withColumn("self_transfer_valid", isNotSelfTransfer)
      .transform(withKnownUserFlag("from_user", "from_user_valid", knownUsers))
      .transform(withKnownUserFlag("to_user", "to_user_valid", knownUsers))
      .withColumn("fee_valid", isFeeValid)
      .withColumn(
        "is_valid",
        $"amount_valid" &&
          $"self_transfer_valid" &&
          $"from_user_valid" &&
          $"to_user_valid" &&
          $"fee_valid"
      )
  }

}
