#!/bin/bash
set -e

mkdir -p /data/spark/events \
    && start-history-server.sh \
    && exec tail -f /dev/null
