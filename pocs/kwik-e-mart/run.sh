#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

DATA_PATH="${DATA_PATH:-/data}"
INFO="\033[0;34mINFO\033[00m:"

echo -e "${INFO} Syncing dependencies..."
if [ -f /.dockerenv ]; then
    export UV_PROJECT_ENVIRONMENT=/opt/venvs/kwik-e-mart
fi
uv sync --frozen

echo -e "${INFO} Starting Spark..."
PYTHONPATH="$(pwd)/src" uv run spark-submit \
    --packages "io.delta:delta-spark_2.13:4.3.1" \
    --conf "spark.sql.debug.maxToStringFields=100" \
    src/kwik_e_mart/main.py \
        --job silver/sales \
        --lake-path "${DATA_PATH}" \
        "$@"

echo -e "${INFO} Process has been finished \\o/"
