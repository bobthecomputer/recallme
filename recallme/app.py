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
    # Allow the application to keep working even if the API is unreachable by
    # falling back to bundled sample data. ``require_api`` is therefore set to
    # ``False`` so a network error won't prevent the page from loading.
    recalls = load_recalls(require_api=False, retries=3)
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
    # Same logic for the demo mode: we prefer using the live API but can
    # gracefully fall back to local data when the network is unavailable.
    recalls = load_recalls(require_api=False, retries=3)
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
    # Retrieve recalls with the same tolerant behaviour as above so the web
    # page can render offline as well.
    recalls = load_recalls(require_api=False, retries=3)
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
