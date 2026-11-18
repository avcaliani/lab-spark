#!/bin/bash
#
# Script Name : run.sh
# Date        : 2026.11
# License     : MIT
#
# Description : Syncs and runs "kwik-e-mart" through Spark Submit.
#               Master, Delta, tuning and logging come from docker/ (spark-defaults.conf, log4j2.properties).
set -euo pipefail
cd "$(dirname "$0")"

DATA_PATH="${DATA_PATH:-/data}"
INFO="\033[0;34mINFO\033[00m:"

# Keep the venv outside the bind-mounted poc, so it never touches the host .venv
export UV_PROJECT_ENVIRONMENT=/opt/venvs/kwik-e-mart

echo -e "${INFO} Syncing dependencies..."
uv sync --frozen

# Event logs for the History Server
mkdir -p "${DATA_PATH}/spark-events"

echo -e "${INFO} Starting Spark..."
PYTHONPATH="$(pwd)/src" uv run spark-submit \
    --packages "io.delta:delta-spark_2.13:4.3.1" \
    --conf "spark.sql.debug.maxToStringFields=100" \
    src/kwik_e_mart/main.py \
        --job silver/sales \
        --lake-path "${DATA_PATH}" \
        "$@"

echo -e "${INFO} Process has been finished \\o/"
