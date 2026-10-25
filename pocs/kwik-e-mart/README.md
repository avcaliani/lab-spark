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

Java, Spark, uv, and all Python dependencies are baked into the image at build time.  
No manual install step after `up`.

```bash
cd pocs/kwik-e-mart

# Build the image
docker compose build

# Start the container
docker compose up -d

# Generate the mock sales dataset
docker compose exec app scripts/generate_sales_data.py

# Run the PySpark job
docker compose exec app scripts/run.sh

# When you're done
docker compose down
```

<details>
<summary>Run locally (without Docker) 👇</summary>

Requires Python 3.12, JDK 21, and [uv](https://docs.astral.sh/uv/) installed locally.

```bash
cd pocs/kwik-e-mart

# Install dependencies
uv sync

# Generate the mock sales dataset
DATA_PATH="$(pwd)/data" scripts/generate_sales_data.py

# Run the PySpark job (must be an absolute path -- Delta's path-based table
# addressing breaks on a leading ./ in the path)
DATA_PATH="$(pwd)/data" scripts/run.sh

# Check the Files
tree ./data -L 4

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
├── Dockerfile
├── docker-compose.yml
├── resources/             # log4j properties
├── scripts/               # data generator and run.sh
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
