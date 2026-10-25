# Kwik-E-Chain

> Part of the [Kwik-E-Mart Universe](../README.md). See there for the inspiration and the other poc.

![License](https://img.shields.io/github/license/avcaliani/lab-spark?color=green)
![Java](https://img.shields.io/badge/Java-21-FF7800?logo=openjdk&logoColor=white)
![Scala](https://img.shields.io/badge/Scala-2.13.18-DC322F?logo=scala&logoColor=white)
![sbt](https://img.shields.io/badge/sbt-1.12.1-1B5162)
![Spark](https://img.shields.io/badge/Apache--Spark-4.1.1-E25A1C?logo=apachespark&logoColor=white)
![Delta Lake](https://img.shields.io/badge/Delta_Lake-4.3.1-00ADD8)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

Scala and Spark pipeline that validates the DonutCoin (DONU) transaction ledger and routes each row to success, error and debug Delta tables.

## Quick Start

```sh
# All commands below run from this folder
cd pocs/kwik-e-chain

# Download the known-users reference (the pipeline reads data/bronze/users.csv to validate transfers)
# Pinned to a commit of kafka-in-docker's Simpsons cast list
mkdir -p data/bronze
curl -o data/bronze/users.csv \
  https://raw.githubusercontent.com/avcaliani/kafka-in-docker/bd46b85779ecc6ee4eebc388813009096bb17158/scripts/users.csv

# Build the image
docker compose build

# Start the container
docker compose up -d

# Generate the mock DonutCoin transactions dataset (python3 is installed in the Dockerfile)
docker compose exec spark python3 scripts/generate_donu_transactions.py

# Run the job (builds & runs)
docker compose exec spark scripts/run.sh

# When you're done
docker compose down
```

<details>
<summary>Pipeline Logs 🎥</summary>

![output](.docs/output.gif)

</details>

<br />

<details>
<summary>Local Development 👇</summary>

Tests and formatting run locally, not inside the container.  
Requires JDK 21 and sbt installed on your machine.

```sh
cd pocs/kwik-e-chain

# Build the project
sbt clean compile package

# Run the tests
sbt test

# Format the code
sbt scalafmtAll
```

</details>

<br />

<details>
<summary>Project Structure 🗂️</summary>

```text
kwik-e-chain/
├── build.sbt
├── Dockerfile
├── docker-compose.yml
├── scripts/               # data generator and run.sh
└── src/
    ├── main/
    │   ├── resources/     # app and log4j2 properties
    │   └── scala/br/avcaliani/kwikechain/
    │       ├── Main.scala
    │       ├── pipelines/
    │       └── utils/
    └── test/scala/        # specs
```

</details>

## Related Links

- [Apache Spark: Official Website](https://spark.apache.org)
- [Delta Lake: Official Website](https://delta.io)
- [SBT Commands](https://alvinalexander.com/scala/sbt-how-to-compile-run-package-scala-project)
- [kafka-in-docker: Simpsons cast reference data](https://github.com/avcaliani/kafka-in-docker)
