import random
import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))
from recallme.main import generate_demo_purchases

SAMPLE_RECALLS = [
    {"name": "Lait entier 1L", "brand": "MarqueX"},
    {"name": "Yaourt nature", "brand": "DairyBest"},
]

def test_demo_always_includes_recall(tmp_path, monkeypatch):
    # Use a minimal CSV so test is fast
    csv = tmp_path / "products.csv"
    df = pd.DataFrame({"ProductName": ["Baguette"], "Brand": ["Boulangerie"]})
    df.to_csv(csv, index=False)

    # Make randomness deterministic
    monkeypatch.setattr(random, "randint", lambda a, b: 1)
    monkeypatch.setattr(random, "sample", lambda seq, k: seq[:k])

    purchases = generate_demo_purchases(SAMPLE_RECALLS, path=str(csv), num_items=1)
    recalled = [p for p in purchases.to_dict(orient="records") if p in SAMPLE_RECALLS]
    assert recalled, "A recalled product should always be included"
