# Kwik-E-Mart

> Part of the [Kwik-E-Mart Universe](../README.md). See there for the inspiration and the other poc.

![License](https://img.shields.io/github/license/avcaliani/lab-spark?color=green)
![Java](https://img.shields.io/badge/Java-21-FF7800?logo=openjdk&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-0.11.29-DE5FE9?logo=astral&logoColor=white)
![Spark](https://img.shields.io/badge/Apache--Spark-4.1.1-E25A1C?logo=apachespark&logoColor=white)
![Delta Lake](https://img.shields.io/badge/Delta_Lake-4.3.1-00ADD8)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

PySpark pipeline that cleans and types the Kwik-E-Mart daily sales.  
The dataset is a locally-generated, dependency-free mock, nothing to download.

## Quick Start

Docker setup lives at the repo root, see [How to run](../../README.md#how-to-run).  
Python deps are synced by `run.sh` into `/opt/venvs/kwik-e-mart` inside the container, so the host `.venv` is never touched.

```bash
# All commands below run from the repo root
docker compose up -d --build

# Generate data and run every poc
docker compose exec spark ./scripts/run-pipeline.sh

# Or, once the data is there, run only this job
docker compose exec spark apps/kwik-e-mart/run.sh

# Check the files
tree data -L 3

# When you're done
docker compose down
```

<details>
<summary>Local Development 👇</summary>

Tests and lint run locally. The job itself runs only in the container (Spark config lives in `docker/spark-defaults.conf`).  
Requires Python 3.12, JDK 21, and [uv](https://docs.astral.sh/uv/) installed locally.

```bash
cd pocs/kwik-e-mart

# Install dependencies
uv sync

# Run the tests
uv run pytest

# Lint
uv run ruff check .
```

</details>

<details>
<summary>Project Structure 🗂️</summary>

```text
kwik-e-mart/
├── pyproject.toml
├── run.sh                 # sync deps + spark-submit
├── src/
│   └── kwik_e_mart/
│       ├── main.py
│       ├── cli.py
│       ├── config.py
│       ├── infra/
│       └── jobs/
└── tests/
```

</details>
