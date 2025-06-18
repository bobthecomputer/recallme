import requests

API_PATH = "/api/explore/v2.1/catalog/datasets/rappelconso-v2-gtin-trie/records"
API_URL = f"https://data.economie.gouv.fr{API_PATH}"


def check_api(limit: int = 5) -> None:
    """Fetch sample data from the RappelConso API and print the result."""
    print("Requesting", API_URL)
    resp = requests.get(
        API_URL,
        params={"limit": limit},
        headers={"Accept": "application/json"},
        timeout=10,
    )
    print("Status:", resp.status_code)
    try:
        data = resp.json()
    except ValueError:
        print("Response was not JSON:")
        print(resp.text[:200])
        return
    results = data.get("results", [])
    print(f"Received {len(results)} results")
    if results:
        print("First result:", results[0])
    else:
        print("No data returned")


if __name__ == "__main__":
    check_api()
