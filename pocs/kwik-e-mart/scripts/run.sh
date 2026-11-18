#!/bin/bash -xe

cd "$(dirname "$0")/.."

# Keep the venv outside the bind-mounted poc, so it never touches the host .venv
export UV_PROJECT_ENVIRONMENT=/opt/venvs/kwik-e-mart
uv sync --frozen

# Event logs for the History Server (spark-defaults.conf)
mkdir -p "${DATA_PATH:-/data}/spark-events"

# Master, Delta and tuning come from spark-defaults.conf
PYTHONPATH="$PWD/src" uv run spark-submit \
  --files resources/log4j.properties \
  --packages "io.delta:delta-spark_2.13:4.3.1" \
  --conf "spark.sql.debug.maxToStringFields=100" \
  --driver-java-options "-Dlog4j2.configurationFile=file:resources/log4j.properties" \
  'src/kwik_e_mart/main.py' \
      --job silver/sales \
      --lake-path "${DATA_PATH:-/data}" \
      "$@"
