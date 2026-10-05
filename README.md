# Docker ML inference demo

Teach Docker entirely in a browser: build an image, run a packaged Python model, change runtime configuration, mount files, inspect caching, and open a container's web page.

**Start with [the instructor demo guide](docs/DEMO.md).**

This is an original, self-contained companion to the Packaging Models Part 2 lesson. It uses the same `load_model()` / `predict()` interface and a JSON smoke test, but does not contain the course's Part 1 source or trained artifact. The model is a tiny scikit-learn sentiment classifier trained on eight examples; it demonstrates packaging, not model quality. No GPU, Hugging Face download, or API key is required.

## Launch in GitHub Codespaces

Open this repository's **Code → Codespaces → Create codespace on main**, choosing a 2-core machine. This lab uses GitHub's default Docker-enabled environment; no custom dev-container rebuild is needed. You need permission to this private repository. Use the Codespaces **terminal** for all commands below, not a notebook Python cell.

```bash
bash scripts/prepare.sh
bash scripts/start-api.sh
```

Open the **Ports** panel and click the browser link for **8080**. Keep port visibility **Private**. Docker's host is the remote Codespace, so laptop `localhost:8080` and laptop data paths are not this environment.

`scripts/prepare.sh` builds `text-inference:dev` and runs the smoke test. The default image command runs that test and exits; the web-server command is an override:

```bash
docker run --rm text-inference:dev
docker run --rm -e MAX_CHARS=10 text-inference:dev
docker run --rm --env-file demo.env text-inference:dev
docker run --rm -v "$PWD/data:/app/data" text-inference:dev python -m text_inference.batch
cat data/predictions.json
```

## Project map

| File | What to show |
| --- | --- |
| `Dockerfile` | Python base, dependency layer, code copy, package install, model artifact, CMD |
| `requirements.txt`, `pyproject.toml` | Pinned model dependencies and installable package |
| `src/text_inference/inference.py` | `load_model()`, `predict()`, `MAX_CHARS` |
| `smoke_test.py` | Structured JSON and known positive/negative examples |
| `src/text_inference/batch.py`, `data/inputs.json` | Read/write files through a bind mount |
| `src/text_inference/serve.py` | A simple HTTP service listening on port 8000 |
| `.dockerignore` | Keep runtime data and secrets out of build context |
| `scripts/verify.py` | Check Docker smoke test, configuration, mounts and API |
| `scripts/cache-demo.sh` | Demonstrate cached dependencies after a source edit |

## Verify or reset

```bash
python scripts/verify.py
bash scripts/cache-demo.sh
bash scripts/cleanup.sh
```

The verification uses a separate temporary API container. Cleanup removes only the two named demonstration containers; it does not prune other Docker resources. To refresh the live API after changing code, rebuild, stop/remove `text-inference-api`, and start it again. A running container keeps its old image even when you rebuild the same tag.

This is a teaching container and standard-library demo HTTP server. Production deployment also needs a proper serving stack, non-root execution, digest-pinned base images, model validation, scanning, secrets management, and operational controls. Python package versions are pinned here; the base tag and build-tool ecosystem can still change over time. GPU commands are discussion-only because this Codespace is CPU-only.

Stop your Codespace after class to stop compute usage. Stored Codespaces still consume storage allowance.
