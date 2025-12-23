import requests

def get_currency() -> list[tuple]:
    """Fetches currency list and formats it for a SelectField dropdown."""
    api_url = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json"
    try:
        response = requests.get(api_url)
        data = response.json()
        # Returns a list of tuples: [('USD', 'United States Dollar'), ...]
        return [(code.upper(), name) for code, name in data.items()]
    except Exception:
        # Fallback if API is down
        return [('USD', 'US Dollar'), ('EUR', 'Euro'), ('GBP', 'British Pound')]