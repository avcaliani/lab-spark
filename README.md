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
├── snippets/                   isolated spark experiments (scripts, notebooks, graphx)
└── pocs/
    ├── README.md               the Kwik-E-Mart universe and the inspiration
    ├── kwik-e-chain/           scala, sbt, delta: validate + route DonutCoin transactions
    └── kwik-e-mart/            pyspark, uv, delta: clean + type Kwik-E-Mart daily sales
```

## How to run

Both pocs live in the same Kwik-E-Mart universe, see [`pocs/README.md`](pocs/README.md).  
Each poc is self-contained and runs in Docker, see its README:

- [`pocs/kwik-e-chain`](pocs/kwik-e-chain/README.md)
- [`pocs/kwik-e-mart`](pocs/kwik-e-mart/README.md)

Experiments are run one by one, see [`snippets/README.md`](snippets/README.md).

---

[Apache Spark] / [Delta Lake] / [sbt] / [uv]

[Apache Spark]: https://spark.apache.org
[Delta Lake]: https://delta.io
[sbt]: https://www.scala-sbt.org
[uv]: https://docs.astral.sh/uv/
