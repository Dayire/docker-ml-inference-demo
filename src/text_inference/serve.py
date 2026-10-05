"""Small HTTP server for port-mapping demos; not a production server."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from .inference import load_model, predict

PAGE = """<!doctype html>
<html lang="en"><meta charset="utf-8"><title>Docker text inference demo</title>
<style>body{font:20px system-ui;max-width:850px;margin:60px auto;padding:20px;background:#f5f8fc;color:#172b4d}input{width:75%;padding:12px;font:inherit}button{padding:12px;font:inherit}pre{white-space:pre-wrap;background:white;padding:24px;border-radius:12px}</style>
<h1>Docker text inference demo</h1>
<p>This page is served by Python inside a Docker container.</p>
<form id="form"><input id="text" value="I love this excellent product" aria-label="Text to classify" required><button>Predict</button></form>
<pre id="result">Click Predict to run the small CPU model.</pre>
<p>A tiny teaching model, trained on eight examples. Predictions are illustrative.</p>
<script>document.getElementById('form').onsubmit=async(e)=>{e.preventDefault();const response=await fetch('/predict?text='+encodeURIComponent(document.getElementById('text').value));document.getElementById('result').textContent=JSON.stringify(await response.json(),null,2);};</script></html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        request = urlparse(self.path)
        if request.path == "/":
            body, content_type, status = PAGE.encode(), "text/html; charset=utf-8", 200
        else:
            try:
                if request.path == "/health":
                    payload, status = {"status": "ok"}, 200
                elif request.path == "/predict":
                    payload = predict(parse_qs(request.query).get("text", [""])[0])
                    status = 200
                else:
                    payload, status = {"error": "not found"}, 404
            except ValueError as exc:
                payload, status = {"error": str(exc)}, 400
            body, content_type = json.dumps(payload).encode(), "application/json"
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    load_model()
    port = int(os.getenv("PORT", "8000"))
    print(f"Teaching server listening on 0.0.0.0:{port}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
