import json
import random
from pathlib import Path

import pandas as pd
import requests


BASE_DIR = Path(__file__).resolve().parent


API_PATH = "/api/explore/v2.1/catalog/datasets/rappelconso-v2-gtin-trie/records"
API_URL = f"https://data.economie.gouv.fr{API_PATH}"


def load_recalls(path="sample_recalls.json", limit=20):
    """Load recall data from the RappelConso API or a local file."""
    try:
        # On tente de récupérer les données depuis l'API
        print("Tentative de récupération des données depuis l'API RappelConso...")
        response = requests.get(f"{API_URL}?limit={limit}", timeout=10)
        response.raise_for_status()  # Lève une exception si le statut est une erreur (4xx ou 5xx)
        data = response.json()
        recalls = []
        for item in data.get("results", []):
            name = item.get("libelle_commercial") # Utilisation de libelle_commercial pour plus de précision
            brand = item.get("marque_produit", "")
            if name:
                recalls.append({"name": name, "brand": brand})
        print("Données récupérées avec succès depuis l'API.")
        return recalls
    except Exception as e:
        # En cas d'échec, on se rabat sur le fichier local
        print(
            f"Erreur lors de la récupération depuis l'API : {e}. "
            "Utilisation des données locales en repli."
        )
        file_path = BASE_DIR / path
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)


def load_purchases(path="purchases.csv"):
    """Charge les achats de l'utilisateur depuis un fichier CSV."""
    file_path = BASE_DIR / path
    # On spécifie le type des colonnes pour éviter les erreurs de comparaison
    return pd.read_csv(file_path, dtype={'name': 'string', 'brand': 'string'})


def generate_demo_purchases(
    recalls,
    path="french_top500_products.csv",
    num_items=20,
    max_recalled=3,
):
    """Generate a random shopping list including a few recalled products."""
    data_path = BASE_DIR / path
    df = pd.read_csv(data_path)
    purchases = df.sample(n=num_items)[["ProductName", "Brand"]]
    purchases.rename(columns={"ProductName": "name", "Brand": "brand"}, inplace=True)

    recall_count = random.randint(0, max_recalled)
    if recall_count:
        recall_sample = random.sample(recalls, k=recall_count)
        recall_df = pd.DataFrame(recall_sample)
        purchases = pd.concat([purchases, recall_df], ignore_index=True)

    return purchases.sample(frac=1).reset_index(drop=True)


def check_recalls(recalls, purchases):
    """Vérifie si des produits achetés correspondent à des rappels."""
    alerts = []
    # Création d'un set pour une recherche plus rapide
    recalled_products = {
        (str(r["name"]).strip().lower(), str(r["brand"]).strip().lower()) for r in recalls
    }

    for index, purchase in purchases.iterrows():
        # Normalisation des données pour une comparaison fiable
        purchase_tuple = (
            str(purchase["name"]).strip().lower(),
            str(purchase["brand"]).strip().lower()
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