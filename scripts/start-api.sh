#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if docker container inspect text-inference-api >/dev/null 2>&1; then
    docker start text-inference-api
else
    docker run -d --name text-inference-api -p 8080:8000 text-inference:dev python -m text_inference.serve
fi
printf '\nOpen the Codespaces Ports panel, then the private browser link for port 8080.\n'
