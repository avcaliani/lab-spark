#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."

DATA_PATH="${DATA_PATH:-/data}"
USERS_URL="https://raw.githubusercontent.com/avcaliani/kafka-in-docker/bd46b85779ecc6ee4eebc388813009096bb17158/scripts/users.csv"

INFO="\033[0;34mINFO\033[00m:"

download_users() {
    local output_dir="${DATA_PATH}/bronze/springfield/users"
    echo -e "${INFO} Downloading users.csv (Springfield cast reference data)..."
    if [ -f "${output_dir}/users.csv" ]; then
        echo -e "${INFO} Already there, skipping."
        return
    fi
    mkdir -p "${output_dir}"
    curl -fsSL -o "${output_dir}/users.csv" "${USERS_URL}"
}

download_users

echo -e "${INFO} Generating mock data..."
uv run --no-project scripts/generate_donu_transactions.py
uv run --no-project scripts/generate_sales_data.py

echo -e "${INFO} Running kwik-e-chain..."
apps/kwik-e-chain/run.sh

echo -e "${INFO} Running kwik-e-mart..."
apps/kwik-e-mart/run.sh

echo -e "${INFO} Pipeline finished \\o/"
