import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))
from recallme.main import load_recalls

class DummyResponse:
    def __init__(self, data, status=200):
        self._data = data
        self.status_code = status

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP error")

    def json(self):
        return self._data


def test_load_recalls_requires_api_failure(monkeypatch):
    def fail_get(*args, **kwargs):
        raise ConnectionError("no network")
    monkeypatch.setattr("requests.get", fail_get)
    with pytest.raises(RuntimeError):
        load_recalls(require_api=True, retries=1)


def test_load_recalls_success(monkeypatch):
    data = {"results": [{"libelle_commercial": "Produit", "marque_produit": "X"}]}
    monkeypatch.setattr("requests.get", lambda *a, **k: DummyResponse(data))
    recalls = load_recalls(require_api=True, retries=1)
    assert recalls == [{"name": "Produit", "brand": "X"}]


def test_load_recalls_retry_until_success(monkeypatch):
    data = {"results": [{"libelle_commercial": "Produit", "marque_produit": "X"}]}
    calls = {"n": 0}

    def flakey_get(*args, **kwargs):
        calls["n"] += 1
        if calls["n"] < 3:
            raise ConnectionError("fail")
        return DummyResponse(data)

    monkeypatch.setattr("requests.get", flakey_get)
    recalls = load_recalls(require_api=True, retries=None)
    assert calls["n"] == 3
    assert recalls == [{"name": "Produit", "brand": "X"}]
