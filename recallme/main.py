import json
import random
from pathlib import Path

import pandas as pd
import requests

BASE_DIR = Path(__file__).resolve().parent

API_PATH = "/api/explore/v2.1/catalog/datasets/rappelconso-v2-gtin-trie/records"
API_URL = f"https://data.economie.gouv.fr{API_PATH}"

FALLBACK_RECALLS = [
    {"name": "Lait entier 1L", "brand": "MarqueX"},
    {"name": "Yaourt nature", "brand": "DairyBest"},
    {"name": "Pain de mie", "brand": "Boulange"},
]
FALLBACK_PRODUCTS = [
    {"ProductName": "Baguette", "Brand": "Boulangerie"},
    {"ProductName": "Eau minérale", "Brand": "Source"},
    {"ProductName": "Lait demi-écrémé", "Brand": "Lactel"},
    {"ProductName": "Pâtes Spaghetti", "Brand": "Barilla"},
    {"ProductName": "Jus d'orange", "Brand": "Tropicana"},
]


def _download_file(url: str, path: Path) -> bool:
    """Download a file if possible. Return True on success."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        path.write_bytes(response.content)
        return True
    except Exception as exc:  # pragma: no cover - network errors
        print(f"Impossible de télécharger {url}: {exc}")
        return False


def load_recalls(path: str = "sample_recalls.json", limit: int = 20):
    """Load recall data from the API with multiple fallbacks."""
    try:
        print("Tentative de récupération des données depuis l'API RappelConso...")
        response = requests.get(f"{API_URL}?limit={limit}", timeout=10)
        response.raise_for_status()
        data = response.json()
        recalls = []
        for item in data.get("results", []):
            name = item.get("libelle_commercial")
            brand = item.get("marque_produit", "")
            if name:
                recalls.append({"name": name, "brand": brand})
        print("Données récupérées avec succès depuis l'API.")
        return recalls
    except Exception as e:  # pragma: no cover - API error fallback
        print(
            f"Erreur lors de la récupération depuis l'API : {e}. "
            "Utilisation des données locales en repli."
        )
        file_path = BASE_DIR / path
        if file_path.exists():
            with file_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        # try to download from GitHub
        url = (
            "https://raw.githubusercontent.com/bobthecomputer/recallme/main/"
            f"recallme/{path}"
        )
        if _download_file(url, file_path):
            with file_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        print("Utilisation d'un petit jeu de données intégré.")
        return FALLBACK_RECALLS


def load_purchases(path: str = "purchases.csv"):
    """Charge les achats de l'utilisateur depuis un fichier CSV."""
    file_path = BASE_DIR / path
    return pd.read_csv(file_path, dtype={"name": "string", "brand": "string"})


def generate_demo_purchases(
    recalls,
    path: str = "french_top500_products.csv",
    num_items: int = 20,
    max_recalled: int = 3,
):
    """Generate a random shopping list including a few recalled products."""
    data_path = BASE_DIR / path
    if not data_path.exists():
        url = (
            "https://raw.githubusercontent.com/bobthecomputer/recallme/main/"
            f"recallme/{path}"
        )
        if not _download_file(url, data_path):
            print("Utilisation d'une liste de produits intégrée.")
            df = pd.DataFrame(FALLBACK_PRODUCTS)
        else:
            df = pd.read_csv(data_path)
    else:
        df = pd.read_csv(data_path)

    purchases = df.sample(n=min(num_items, len(df)))[["ProductName", "Brand"]]
    purchases.rename(columns={"ProductName": "name", "Brand": "brand"}, inplace=True)

    if recalls:
        recall_count = random.randint(1, min(max_recalled, len(recalls)))
        recall_sample = random.sample(recalls, k=recall_count)
        recall_df = pd.DataFrame(recall_sample)
        purchases = pd.concat([purchases, recall_df], ignore_index=True)

    return purchases.sample(frac=1).reset_index(drop=True)



def check_recalls(recalls, purchases):
    """Vérifie si des produits achetés correspondent à des rappels."""
    alerts = []
    recalled_products = {
        (str(r["name"]).strip().lower(), str(r["brand"]).strip().lower()) for r in recalls
    }

    for _, purchase in purchases.iterrows():
        purchase_tuple = (
            str(purchase["name"]).strip().lower(),
            str(purchase["brand"]).strip().lower(),
        )
        if purchase_tuple in recalled_products:
            alerts.append(purchase.to_dict())
    return alerts


def main():
    """Fonction principale du script."""
    recalls = load_recalls()
    print("\n--- Derniers rappels connus ---")
    if not recalls:
        print("Aucun rappel à afficher.")
    else:
        for rec in recalls:
            brand = f" (Marque : {rec['brand']})" if rec.get("brand") else ""
            print(f"- {rec['name']}{brand}")
    print("-" * 30)

    purchases = load_purchases()
    alerts = check_recalls(recalls, purchases)

    if alerts:
        print("\n⚠️ ALERTE : Produits rappelés trouvés dans vos achats !")
        for item in alerts:
            print(f"- {item['name']} (Marque : {item['brand']})")
    else:
        print("\n✅ Bonne nouvelle ! Aucun produit rappelé parmi vos achats.")


if __name__ == "__main__":
    main()
