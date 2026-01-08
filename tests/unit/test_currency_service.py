from Splity.services import currency_service


def test_get_currency_fallback_on_failure(monkeypatch):
    def raise_error(_url):
        raise RuntimeError("network error")

    monkeypatch.setattr(currency_service.requests, "get", raise_error)

    currencies = currency_service.get_currency()

    assert ("USD", "US Dollar") in currencies
    assert ("EUR", "Euro") in currencies
    assert ("GBP", "British Pound") in currencies
