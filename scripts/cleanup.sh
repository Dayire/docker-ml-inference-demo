#!/usr/bin/env bash
set -euo pipefail
# Remove only this demo's explicitly named, disposable containers.
for name in text-inference-api lesson-smoke; do
    if docker container inspect "$name" >/dev/null 2>&1; then
        docker stop "$name" >/dev/null
        docker rm "$name"
    fi
done
printf 'Demo containers removed; built images and project files remain.\n'
