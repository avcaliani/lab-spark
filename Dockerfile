FROM eclipse-temurin:21-jdk

# Versions 👇
ENV SPARK_VERSION="4.1.1"
ENV HADOOP_VERSION="3"
ENV SBT_VERSION="1.12.1"
ENV PYTHON_VERSION="3.12"

# Spark 👇
ENV SPARK_HOME="/opt/spark"
ENV PATH="$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH"

# sbt 👇
ENV SBT_HOME="/opt/sbt"
ENV PATH="$SBT_HOME/bin:$PATH"

# Python / uv 👇
ENV UV_PYTHON="$PYTHON_VERSION"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYSPARK_PYTHON=python

WORKDIR /opt

# uv + Python
COPY --from=ghcr.io/astral-sh/uv:0.11.29 /uv /uvx /bin/
RUN uv python install "$PYTHON_VERSION"

# sbt
ADD "https://github.com/sbt/sbt/releases/download/v${SBT_VERSION}/sbt-${SBT_VERSION}.tgz" .
RUN tar -xzf sbt-*.tgz && rm -f sbt-*.tgz

# Spark
ADD "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" .
RUN tar -xzf spark-*.tgz && rm -f spark-*.tgz && mv spark-* spark

WORKDIR /opt/spark-apps

CMD ["tail", "-f", "/dev/null"]
