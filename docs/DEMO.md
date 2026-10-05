# Instructor run sheet: 25–35 minutes

Run commands in the Codespaces terminal from the repository root. Keep the Ports panel private. Ask learners to predict the result before you run each command.

## Before class

```bash
bash scripts/prepare.sh
python scripts/verify.py
bash scripts/start-api.sh
```

Open the forwarded port 8080 and try `I love this excellent product`. Check it also gives `negative` for `I hate this terrible product`. After preparation, the main build will be cached. To show a real first build, use `docker build --no-cache --progress=plain -t text-inference:dev .` before class or allow time during the demo.

## 1. Image vs container — 4 minutes

```bash
docker images text-inference
docker run --name lesson-smoke text-inference:dev
docker ps
docker ps -a --filter name=lesson-smoke
docker logs lesson-smoke
docker start -a lesson-smoke
docker rm lesson-smoke
```

Expected: JSON with `status: ok`, one positive and one negative prediction. The command finishes, so the container appears in `ps -a`, not `ps`. Its logs and filesystem survive until removal; removing it leaves the image. If the name already exists from rehearsal, inspect it, then remove that stopped demo container before rerunning.

Ask: **Why does `docker ps` show no smoke-test container?**

## 2. Dockerfile and build — 5 minutes

Open `Dockerfile` and explain `FROM → WORKDIR → COPY → RUN → CMD`.

```bash
docker build --progress=plain -t text-inference:dev .
docker history text-inference:dev
docker run --rm text-inference:dev python --version
docker run --rm -it text-inference:dev bash
```

In the container shell, run `pwd` and `ls`, then `exit`. This overrides CMD. The model is generated during build only to keep this companion demo self-contained; ordinarily you copy a trained, trusted artifact into the image. Some Dockerfile instructions set metadata rather than adding filesystem layers.

Ask: **What would changing CMD alter, and what would changing requirements alter?**

## 3. Same image, different configuration — 4 minutes

```bash
docker run --rm text-inference:dev
docker run --rm -e MAX_CHARS=10 text-inference:dev
docker run --rm --env-file demo.env text-inference:dev
```

Expected: `max_chars` changes from 200 to 10, `text_used` becomes the first 10 characters and `truncated` becomes true. The image is unchanged. `demo.env` contains only a non-secret teaching setting.

Ask: **Why is no rebuild necessary?**

## 4. Bind mount — 4 minutes

```bash
cat data/inputs.json
docker run --rm -v "$PWD/data:/app/data" text-inference:dev python -m text_inference.batch
cat data/predictions.json
```

Expected: three predictions are written to the Codespace's `data/predictions.json`. The container is removed by `--rm`, but the mounted output survives. `data/` is excluded from the image by `.dockerignore`; the mount supplies it at runtime. Change an input in the editor and rerun without rebuilding.

Ask: **Where does this output live: laptop, Codespace, or image?** Answer: on the Codespace's mounted filesystem.

## 5. Ports, detached services and logs — 5 minutes

```bash
bash scripts/start-api.sh
docker ps --filter name=text-inference-api
docker logs text-inference-api
curl -fsS http://localhost:8080/health
docker exec text-inference-api printenv MAX_CHARS
```

Open **Ports → 8080 → Open in Browser** and submit a prediction. `8080:8000` maps the cloud host's port 8080 to Python's port 8000 inside the container. Python listens on `0.0.0.0`, not only container loopback. `localhost` in this terminal refers to the cloud host.

```bash
docker stop text-inference-api
docker ps -a --filter name=text-inference-api
docker start text-inference-api
```

Refresh the page after the server restarts. Container lifetime is independent of the browser tab. Keep this endpoint private for the instructor demo.

## 6. Build cache — 4 minutes

```bash
bash scripts/cache-demo.sh
```

The script first builds the original source, appends a harmless source comment, builds a separate `text-inference:cache-demo` image, and restores the file. In the second build, the requirements-install step remains **CACHED**, while source-copy and package-install steps rerun. Logs remain under `/tmp/docker-demo-cache/`. This does not change the live `text-inference:dev` tag.

Ask: **If requirements changed instead, which later steps would rerun?**

## Close

```bash
bash scripts/cleanup.sh
```

Stop the Codespace from GitHub after class. Keep GPU base images and `--gpus all` as a discussion point, since this environment has no GPU. For a production discussion, distinguish a working teaching container from validated model behavior, a production server, secure deployment and operations.
