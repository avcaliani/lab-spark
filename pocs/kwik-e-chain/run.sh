#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

DATA_PATH="${DATA_PATH:-/data}"
INFO="\033[0;34mINFO\033[00m:"

echo -e "${INFO} Building project..."
sbt assembly

jar_file=$(ls target/scala-*/*.jar)
echo -e "${INFO} JAR File -> '${jar_file}'"

echo -e "${INFO} Starting Spark..."
spark-submit \
    "${jar_file}" -p daily-transactions "$@"

echo -e "${INFO} Process has been finished \\o/"
