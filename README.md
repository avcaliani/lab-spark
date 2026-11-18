<img src=".docs/spark-logo.svg" align="right" height="64px"/>

# Spark Lab

![Spark](https://img.shields.io/badge/Apache--Spark-4.1.1-E25A1C?style=flat&logo=apachespark&logoColor=white)
![Delta Lake](https://img.shields.io/badge/Delta_Lake-4.3.1-00ADD8?style=flat)
![Scala](https://img.shields.io/badge/Scala-2.13-DC322F?style=flat&logo=scala&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat&logo=opensourceinitiative&logoColor=white)

Personal [Apache Spark](https://spark.apache.org) learning sandbox, in Scala and PySpark.

## Structure

```text
.
├── .docs/                      readme assets
├── .github/                    pr + issue templates
├── AGENTS.md                   instructions for coding agents
├── LICENSE                     MIT license
├── docker/
│   ├── Dockerfile              one image for both pocs: java, spark, sbt, uv
│   ├── spark-defaults.conf     local spark tuning, baked into the image
│   └── start.sh                container cmd: starts the history server, stays alive
├── docker-compose.yml          one long-running container, exec into it
├── data/                       shared data lake (bronze, silver, gold), gitignored
├── scripts/
│   ├── run-pipeline.sh         generate data, then run every poc
│   └── generate_*.py           mock data generators
└── pocs/
    ├── README.md               the Kwik-E-Mart universe and the inspiration
    ├── kwik-e-chain/           scala, sbt, delta: validate + route DonutCoin transactions
    └── kwik-e-mart/            pyspark, uv, delta: clean + type Kwik-E-Mart daily sales
```

## How to run

Both pocs live in the same Kwik-E-Mart universe and share one image and one data lake, see [`pocs/README.md`](pocs/README.md).  
Everything runs from the repo root:

```bash
docker compose up -d --build                             # build image, start container (rerun after docker/ edits)
docker compose exec spark ./scripts/run-pipeline.sh      # generate data + run every poc
docker compose exec spark apps/kwik-e-mart/scripts/run.sh # one poc
docker compose exec spark bash                           # poke around
docker compose down                                      # stop + remove container
```

> [!TIP]
> **Spark UIs**
>
> - [localhost:4040](http://localhost:4040): Spark UI, only while a job is running.
> - [localhost:18080](http://localhost:18080): Spark History Server, browse finished jobs.

Inside the container `pocs/` is mounted at `/opt/spark-apps/apps` and `data/` at `/data`.  
See each poc's README for details:

- [`pocs/kwik-e-chain`](pocs/kwik-e-chain/README.md)
- [`pocs/kwik-e-mart`](pocs/kwik-e-mart/README.md)

Small isolated experiments live in [scratchpad](https://github.com/avcaliani/scratchpad/tree/main/data/spark).

---

[Apache Spark] / [Delta Lake] / [sbt] / [uv]

[Apache Spark]: https://spark.apache.org
[Delta Lake]: https://delta.io
[sbt]: https://www.scala-sbt.org
[uv]: https://docs.astral.sh/uv/

---

> [!NOTE]
> **AI Disclaimer**
>
> This is a study repo, and the goal is learning and sharpening my skills, so most of the code is written by me.  
> I use LLMs to explain concepts, help with code and tests, review code, improve docs and notes,
> and assist with refactors, including reorganizing files.  
> I personally review all changes and take responsibility for them.
