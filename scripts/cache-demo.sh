#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
logdir=/tmp/docker-demo-cache
mkdir -p "$logdir"
source_file=src/text_inference/inference.py
backup=$(mktemp)
cp "$source_file" "$backup"
trap 'cp "$backup" "$source_file"; rm -f "$backup"' EXIT
printf 'First build: original source\n'
docker build --progress=plain -t text-inference:cache-demo . 2>&1 | tee "$logdir/before.log"
printf '\n# Harmless source change for the cache demonstration.\n' >> "$source_file"
printf '\nSecond build: code changed, dependencies unchanged\n'
docker build --progress=plain -t text-inference:cache-demo . 2>&1 | tee "$logdir/after.log"
printf '\nLook for CACHED on the requirements-install step; source copy and package install rerun.\n'
printf 'Original source restored automatically; logs: %s\n' "$logdir"
