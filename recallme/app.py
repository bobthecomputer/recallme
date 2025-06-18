from flask import Flask, render_template, request
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

USE_PROXY = None
if os.getenv("RECALLME_NO_PROXY"):
    USE_PROXY = False

try:  # Support execution with `python app.py`
    from .main import (
        load_recalls,
        load_purchases,
        generate_demo_purchases,
    )  # type: ignore
except ImportError:  # pragma: no cover - fallback for direct script execution
    import sys

    sys.path.append(str(BASE_DIR))
    from main import load_recalls, load_purchases, generate_demo_purchases

def merge_data():
    # For the demo we always fetch data from the API. If it échoue, an error
    # page is displayed instead of falling back to sample data.
    recalls = load_recalls(require_api=True, retries=3, use_proxy=USE_PROXY)
    purchases = load_purchases()
    results = []
    for _, row in purchases.iterrows():
        recalled = any(
            rec["name"] == row["name"] and rec["brand"] == row["brand"]
            for rec in recalls
        )
        results.append(
            {
                "name": row["name"],
                "brand": row["brand"],
                "recalled": recalled,
            }
        )
    return results, recalls


def merge_demo_data(num_items=20):
    # Demo purchases also rely solely on live data. Any network failure causes
    # an exception instead of silently using bundled samples.
    recalls = load_recalls(require_api=True, retries=3, use_proxy=USE_PROXY)
    purchases = generate_demo_purchases(recalls, num_items=num_items)
    results = []
    for _, row in purchases.iterrows():
        recalled = any(
            rec["name"] == row["name"] and rec["brand"] == row["brand"]
            for rec in recalls
        )
        results.append(
            {
                "name": row["name"],
                "brand": row["brand"],
                "recalled": recalled,
            }
        )
    return results, recalls

app = Flask(__name__)

@app.route("/")
def index():
    # Retrieve recalls directly from the API. Failure to connect results in an
    # error instead of falling back to bundled data.
    recalls = load_recalls(require_api=True, retries=3, use_proxy=USE_PROXY)
    logo_exists = (STATIC_DIR / "logo.png").exists()
    # No purchase list by default; users can try the demo instead
    return render_template("index.html", results=[], recalls=recalls, logo_exists=logo_exists)


@app.route("/demo")
def demo():
    num = int(request.args.get("n", 20))
    results, recalls = merge_demo_data(num)
    logo_exists = (STATIC_DIR / "logo.png").exists()
    return render_template("index.html", results=results, recalls=recalls, logo_exists=logo_exists)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Serve the RecallMe demo")
    parser.add_argument(
        "--no-proxy",
        action="store_true",
        help="ignore HTTP(S)_PROXY variables (or set RECALLME_NO_PROXY=1)",
    )
    parser.add_argument(
        "--use-proxy",
        dest="no_proxy",
        action="store_false",
        help="force proxy usage even if RECALLME_NO_PROXY is set",
    )
    args = parser.parse_args()

    global USE_PROXY
    if args.no_proxy:
        USE_PROXY = False

    # The reloader can spawn multiple processes which may leave the port busy
    # if the server is interrupted. Disabling it avoids the common "address
    # already in use" error when restarting.
    app.run(debug=True, host="0.0.0.0", use_reloader=False)