import argparse
import json
from pathlib import Path
from .inference import predict

parser = argparse.ArgumentParser()
parser.add_argument("--input", default="/app/data/inputs.json")
parser.add_argument("--output", default="/app/data/predictions.json")
args = parser.parse_args()
texts = json.loads(Path(args.input).read_text())
output = Path(args.output)
output.write_text(json.dumps([predict(text) for text in texts], indent=2) + "\n")
print(f"Wrote {len(texts)} predictions to {output}")
