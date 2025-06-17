import json
from pathlib import Path

import pandas as pd
import requests


BASE_DIR = Path(__file__).resolve().parent


API_PATH = "/api/explore/v2.1/catalog/datasets/rappelconso-v2-gtin-trie/records"
API_URL = f"https://data.economie.gouv.fr{API_PATH}"


def load_recalls(path="sample_recalls.json", limit=20):
    """Load recall data from the RappelConso API or a local file."""
    try:
        response = requests.get(f"{API_URL}?limit={limit}", timeout=10)
        response.raise_for_status()
        data = response.json()
        recalls = []
        for item in data.get("results", []):
            name = item.get("libelle")
            brand = item.get("marque_produit", "")
            if name:
                recalls.append({"name": name, "brand": brand})
        return recalls
    except Exception as e:
        print(
            f"Erreur lors de la récupération depuis l'API : {e}. "
            "Utilisation des données locales."
        )
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
    print("Derniers rappels connus :")
    for rec in recalls:
        brand = f" ({rec['brand']})" if rec.get("brand") else ""
        print(f"- {rec['name']}{brand}")
    print()

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
