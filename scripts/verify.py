"""Exercise the container as a consumer: no local model installation required."""
import json
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGE = "text-inference:dev"


def docker(*args):
    return subprocess.check_output(["docker", *args], cwd=ROOT, text=True)


def request(url):
    with urllib.request.urlopen(url, timeout=3) as response:
        return json.load(response)


result = json.loads(docker("run", "--rm", IMAGE))
assert result["status"] == "ok"
assert [r["label"] for r in result["predictions"]] == ["positive", "negative"]
print("PASS: packaged model smoke test")

for flags in [("-e", "MAX_CHARS=10"), ("--env-file", "demo.env")]:
    result = json.loads(docker("run", "--rm", *flags, IMAGE))
    assert all(r["max_chars"] == 10 and r["truncated"] and len(r["text_used"]) == 10 for r in result["predictions"])
print("PASS: runtime environment flag and env file")

# Put scratch data within /workspaces so Codespaces Docker bind mounts resolve.
with tempfile.TemporaryDirectory(prefix="verify-", dir=ROOT / "data") as directory:
    path = Path(directory)
    texts = ["I love this excellent product", "I hate this terrible product"]
    (path / "inputs.json").write_text(json.dumps(texts))
    docker("run", "--rm", "-v", f"{path}:/app/data", IMAGE, "python", "-m", "text_inference.batch")
    predictions = json.loads((path / "predictions.json").read_text())
    assert [r["label"] for r in predictions] == ["positive", "negative"]
print("PASS: bind-mounted input and persistent output")

container = docker("run", "-d", "-p", "127.0.0.1::8000", IMAGE, "python", "-m", "text_inference.serve").strip()
try:
    mapping = docker("port", container, "8000/tcp").strip()
    url = f"http://{mapping}"
    for attempt in range(30):
        try:
            assert request(url + "/health")["status"] == "ok"
            break
        except (urllib.error.URLError, TimeoutError, ConnectionResetError, ConnectionAbortedError):
            time.sleep(0.5)
    else:
        raise RuntimeError("API did not become healthy")
    assert request(url + "/predict?text=excellent%20wonderful")["label"] == "positive"
    assert request(url + "/predict?text=terrible%20awful")["label"] == "negative"
    try:
        request(url + "/predict?text=")
        raise AssertionError("empty text should return HTTP 400")
    except urllib.error.HTTPError as error:
        assert error.code == 400
    print("PASS: port mapping, health, API predictions and invalid input")
finally:
    docker("stop", container)
    docker("rm", container)
print("ALL DEMO CHECKS PASSED")
