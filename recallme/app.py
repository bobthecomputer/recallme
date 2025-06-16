from flask import Flask, render_template

try:  # Support execution with `python app.py`
    from .main import load_recalls, load_purchases  # type: ignore
except ImportError:  # pragma: no cover - fallback for direct script execution
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parent))
    from main import load_recalls, load_purchases

def merge_data():
    recalls = load_recalls()
    purchases = load_purchases()
    results = []
    for _, row in purchases.iterrows():
        recalled = any(
            rec["name"] == row["name"] and rec["brand"] == row["brand"]
            for rec in recalls
        )
        results.append({
            "name": row["name"],
            "brand": row["brand"],
            "recalled": recalled,
        })
    return results

app = Flask(__name__)

@app.route("/")
def index():
    results = merge_data()
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
