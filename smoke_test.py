import json
from text_inference import load_model, predict

load_model()
results = [predict("I love this excellent product"), predict("I hate this terrible product")]
assert [r["label"] for r in results] == ["positive", "negative"]
print(json.dumps({"status": "ok", "predictions": results}, indent=2))
