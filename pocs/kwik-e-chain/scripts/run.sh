#!/bin/bash
#
# Script Name : run.sh
# Date        : 2026.07
# License     : MIT
#
# Description : Runs "kwik-e-chain" through Spark Submit.
cd "$(dirname "$0")/.."

JAR_DIR="target/scala-*"

INFO="\033[0;34mINFO\033[00m:"
ERROR="\033[0;31mERROR\033[00m:"


# =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=
#  FUNCTIONS
# =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=

is_installed() {
    if [ -z $(command -v $1) ]; then
      echo -e "${ERROR} '$1' not found, please check it first."
      exit 0
    fi
}


# =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=
#  RUNNING...
# =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=

echo "
   ___                   _
  / __| _ __  __ _  _ _ | |__
  \\__ \\| '_ \/ _\` || '_|| / /
  |___/| .__/\\__,_||_|  |_\\_\\
       |_|      APP v26.07.00
"

is_installed "java"
is_installed "spark-submit"
is_installed "sbt"

echo -e "${INFO} Building project..."
sbt clean assembly

jar_file=$(ls ${JAR_DIR}/*.jar)
echo -e "${INFO} JAR File -> '${jar_file}'"

log4j_config="file://$(pwd)/src/main/resources/log4j2.properties"

echo -e "${INFO} Starting Spark..."
spark-submit \
    --master local \
    --conf "spark.driver.extraJavaOptions=-Dlog4j.configurationFile=${log4j_config}" \
    --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
    --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" \
    ${jar_file} \
    -p daily-transactions "$@"

echo -e "${INFO} Process has been finished \\o/"
