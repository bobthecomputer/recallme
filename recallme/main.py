import json
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def load_recalls(path="sample_recalls.json"):
    file_path = BASE_DIR / path
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_purchases(path="purchases.csv"):
    file_path = BASE_DIR / path
    return pd.read_csv(file_path)


def check_recalls(recalls, purchases):
    alerts = []
    for recall in recalls:
        match = purchases[(purchases["name"] == recall["name"]) & (purchases["brand"] == recall["brand"])]
        if not match.empty:
            alerts.append(recall)
    return alerts


def main():
    recalls = load_recalls()
    purchases = load_purchases()
    alerts = check_recalls(recalls, purchases)
    if alerts:
        print("Produits rappelés trouvés :")
        for item in alerts:
            print(f"- {item['name']} ({item['brand']})")
    else:
        print("Aucun produit rappelé parmi vos achats.")


if __name__ == "__main__":
    main()
