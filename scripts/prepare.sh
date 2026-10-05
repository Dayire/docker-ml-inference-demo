#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker version
docker build --progress=plain -t text-inference:dev .
docker run --rm text-inference:dev
printf '\nReady. Follow docs/DEMO.md for the live teaching sequence.\n'
