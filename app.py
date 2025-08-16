from flask import Flask, request, jsonify
import subprocess
import os
import uuid
import json

app = Flask(__name__)

def is_http_url(url: str) -> bool:
    from urllib.parse import urlparse
    try:
        u = urlparse(url)
        return u.scheme in ("http", "https")
    except:
        return False

@app.route("/scan", methods=["GET"])
def scan():
    url = request.args.get("url", "https://test.vn")
    if not is_http_url(url):
        return jsonify({"error": "Invalid URL, must start with http(s)"}), 400

    # Unique output filename to avoid collisions
    out_file = f"/tmp/wappalyzer-{uuid.uuid4()}.json"

    try:
        # Run wappalyzer
        subprocess.run(
            ["wappalyzer", "-i", url,"--scan-type balanced", "-oJ", out_file],
            check=True,
            timeout=90
        )

        # Read output file
        with open(out_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        return jsonify(data)

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Wappalyzer failed", "detail": str(e)}), 500
    except FileNotFoundError:
        return jsonify({"error": "Output file not found"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            os.remove(out_file)
        except:
            pass

@app.route("/")
def index():
    return "Wappalyzer API running. Use /scan?url=https://example.com"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
