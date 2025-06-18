import os
import requests
import argparse

API_PATH = "/api/explore/v2.1/catalog/datasets/rappelconso-v2-gtin-trie/records"
API_URL = f"https://data.economie.gouv.fr{API_PATH}"


def check_api(limit: int = 5, *, use_proxy: bool | None = None) -> None:
    """Fetch sample data from the RappelConso API and print the result."""
    if use_proxy is None and os.getenv("RECALLME_NO_PROXY"):
        use_proxy = False

    print("Requesting", API_URL)
    if use_proxy is False:
        proxies = {"http": None, "https": None}
    else:
        proxies = None
    env_proxy = os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY")
    if env_proxy:
        print("Using proxy:", env_proxy if use_proxy is not False else "disabled")
    resp = requests.get(
        API_URL,
        params={"limit": limit, "order_by": "date_publication desc"},
        headers={"Accept": "application/json"},
        timeout=10,
        proxies=proxies,
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
    import argparse

    parser = argparse.ArgumentParser(description="Test the RappelConso API")
    parser.add_argument("--limit", type=int, default=5, help="number of results")
    parser.add_argument(
        "--no-proxy",
        action="store_true",
        help="ignore HTTP(S)_PROXY environment variables",
    )
    parser.add_argument(
        "--use-proxy",
        dest="no_proxy",
        action="store_false",
        help="force proxy usage even if RECALLME_NO_PROXY is set",
    )
    args = parser.parse_args()
    check_api(limit=args.limit, use_proxy=False if args.no_proxy else None)