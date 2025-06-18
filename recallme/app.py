from flask import Flask, render_template, request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

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
    recalls = load_recalls(require_api=True, retries=3)
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
    recalls = load_recalls(require_api=True, retries=3)
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
    recalls = load_recalls(require_api=True, retries=3)
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
    # The reloader can spawn multiple processes which may leave the port busy
    # if the server is interrupted. Disabling it avoids the common "address
    # already in use" error when restarting.
    app.run(debug=True, host="0.0.0.0", use_reloader=False)
