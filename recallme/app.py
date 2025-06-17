from flask import Flask, render_template, request

try:  # Support execution with `python app.py`
    from .main import (
        load_recalls,
        load_purchases,
        generate_demo_purchases,
    )  # type: ignore
except ImportError:  # pragma: no cover - fallback for direct script execution
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parent))
    from main import load_recalls, load_purchases, generate_demo_purchases

def merge_data():
    recalls = load_recalls()
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
    recalls = load_recalls()
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
    recalls = load_recalls()
    # No purchase list by default; users can try the demo instead
    return render_template("index.html", results=[], recalls=recalls)


@app.route("/demo")
def demo():
    num = int(request.args.get("n", 20))
    results, recalls = merge_demo_data(num)
    return render_template("index.html", results=results, recalls=recalls)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

