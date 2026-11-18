#!/bin/bash
#
# Script Name : run-pipeline.sh
# Date        : 2026.11
# License     : MIT
#
# Description : Generates the mock data and runs every poc, in order.
#               Meant to run inside the container (see docker-compose.yml).
set -euo pipefail
cd "$(dirname "$0")/.."

DATA_PATH="${DATA_PATH:-/data}"
# Pinned to a commit of kafka-in-docker's Simpsons cast list
USERS_URL="https://raw.githubusercontent.com/avcaliani/kafka-in-docker/bd46b85779ecc6ee4eebc388813009096bb17158/scripts/users.csv"

INFO="\033[0;34mINFO\033[00m:"

echo -e "${INFO} Downloading users.csv (kwik-e-chain reference data)..."
if [ -f "${DATA_PATH}/bronze/users.csv" ]; then
  echo -e "${INFO} Already there, skipping."
else
  mkdir -p "${DATA_PATH}/bronze"
  curl -fsSL -o "${DATA_PATH}/bronze/users.csv" "${USERS_URL}"
fi

echo -e "${INFO} Generating mock data..."
uv run --no-project scripts/generate_donu_transactions.py
uv run --no-project scripts/generate_sales_data.py

echo -e "${INFO} Running kwik-e-chain..."
apps/kwik-e-chain/scripts/run.sh

echo -e "${INFO} Running kwik-e-mart..."
apps/kwik-e-mart/scripts/run.sh

echo -e "${INFO} Pipeline finished \\o/"
