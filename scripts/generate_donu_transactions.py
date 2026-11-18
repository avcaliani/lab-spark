#!/usr/bin/env -S uv run --script
# Generates a mock "DonutCoin (DONU)" transaction ledger dataset, themed on The Simpsons.
#
# Output: $DATA_PATH/bronze/kwik_e_chain/transactions/donu/.
# Env Vars:
#   - NUM_TRANSACTIONS (default 1000000)
#   - NUM_FILES (default 10)
#   - DATA_PATH (default /data)
#
import csv
import os
import random
import sys
import time
import uuid
from pathlib import Path

MIN_ROWS_PER_FILE = 1000
INVALID_PCT = 5

USERS = [
    "Homer Simpson", "Marge Simpson", "Bart Simpson", "Lisa Simpson",
    "Maggie Simpson", "Ned Flanders", "Milhouse Van Houten", "Mr. Burns",
    "Waylon Smithers", "Krusty the Clown", "Apu Nahasapeemapetilon",
    "Principal Skinner", "Edna Krabappel", "Chief Wiggum", "Ralph Wiggum",
    "Groundskeeper Willie", "Comic Book Guy", "Moe Szyslak", "Lenny Leonard",
    "Carl Carlson",
]
UNKNOWN_USER = "Snowball (Unknown)"

CSV_HEADER = ["transaction_id", "timestamp", "from_user", "to_user", "amount_cents", "currency", "fee_cents"]


def maybe_buggy(txn: dict) -> dict:

    if random.randint(0, 99) >= INVALID_PCT:
        return txn

    match random.randint(0, 2):
        case 0:
            txn["to_user"] = txn["from_user"]
        case 1:
            which_user = "to_user" if random.randint(0, 1) == 0 else "from_user"
            txn[which_user] = UNKNOWN_USER
        case _:
            curr_amount = txn["amount_cents"]
            txn["amount_cents"] = -curr_amount
            txn["fee_cents"] = -curr_amount // 20

    return txn


def new_row() -> list[str | int]:
    amount_cents = random.randint(100, 1000000)
    timestamp = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ",
        time.gmtime(int(time.time()) - random.randint(0, 90 * 24 * 3600))
    )
    new_txn = maybe_buggy({
        "transaction_id": str(uuid.uuid4()),
        "timestamp": timestamp,
        "from_user": random.choice(USERS),
        "to_user": random.choice(USERS),
        "amount_cents": amount_cents,
        "currency": "DONU",
        "fee_cents": amount_cents // 20,
    })
    return [new_txn[col] for col in CSV_HEADER]


def main() -> None:
    num_transactions = int(os.environ.get("NUM_TRANSACTIONS", 1000000))
    num_files_requested = int(os.environ.get("NUM_FILES", 10))
    data_path = os.environ.get("DATA_PATH", "/data")
    output_dir = Path(data_path) / "bronze" / "kwik_e_chain" / "transactions" / "donu"

    if num_transactions < 1:
        sys.exit(f"NUM_TRANSACTIONS must be >= 1 (got {num_transactions})")
    if num_files_requested < 1:
        sys.exit(f"NUM_FILES must be >= 1 (got {num_files_requested})")

    max_files_by_rows = max(num_transactions // MIN_ROWS_PER_FILE, 1)
    num_files = min(num_files_requested, max_files_by_rows)
    if num_files < num_files_requested:
        print(f"Capping NUM_FILES {num_files_requested} -> {num_files}")

    output_dir.mkdir(parents=True, exist_ok=True)

    base_rows = num_transactions // num_files
    extra_rows = num_transactions % num_files

    for file_idx in range(num_files):
        rows_in_file = base_rows + (1 if file_idx < extra_rows else 0)

        part_file = output_dir / f"part-{file_idx:05d}.csv"
        with part_file.open("w", newline="") as new_file:
            writer = csv.writer(new_file)
            writer.writerow(CSV_HEADER)
            for _ in range(rows_in_file):
                writer.writerow(new_row())
        print(f"Wrote {rows_in_file} rows -> {part_file}")

    print(f"Done. NUM_TRANSACTIONS={num_transactions} NUM_FILES={num_files} -> {output_dir}")


if __name__ == "__main__":
    main()
