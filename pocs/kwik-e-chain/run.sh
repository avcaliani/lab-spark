#!/bin/bash
#
# Script Name : run.sh
# Date        : 2026.07
# License     : MIT
#
# Description : Builds and runs "kwik-e-chain" through Spark Submit.
#               Master, Delta, tuning and logging come from docker/ (spark-defaults.conf, log4j2.properties).
set -euo pipefail
cd "$(dirname "$0")"

DATA_PATH="${DATA_PATH:-/data}"
INFO="\033[0;34mINFO\033[00m:"

echo -e "${INFO} Building project..."
sbt assembly
jar_file=$(ls target/scala-*/*.jar)
echo -e "${INFO} JAR File -> '${jar_file}'"

# Event logs for the History Server
mkdir -p "${DATA_PATH}/spark-events"

echo -e "${INFO} Starting Spark..."
spark-submit \
    "${jar_file}" \
        -p daily-transactions \
        "$@"

echo -e "${INFO} Process has been finished \\o/"
