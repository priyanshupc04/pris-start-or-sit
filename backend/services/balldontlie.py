import os
import requests

BASE_URL = "https://api.balldontlie.io/v1"


def _headers() -> dict:
    api_key = os.getenv("BALLDONTLIE_API_KEY")
    if not api_key:
        raise ValueError(
            "Missing BALLDONTLIE_API_KEY. Set it in terminal:\n"
            'export BALLDONTLIE_API_KEY="YOUR_KEY_HERE"'
        )
    return {"Authorization": api_key}


def _api_search(query: str) -> list[dict]:
    r = requests.get(
        f"{BASE_URL}/players",
        params={"search": query},
        headers=_headers(),
        timeout=15,
    )
    r.raise_for_status()
    return r.json().get("data", [])


def search_player(name: str) -> dict:
    """
    Finds a player from a user-typed name.
    Works for:
      - "LeBron"
      - "James"
      - "LeBron James"
    """
    raw = name.strip()
    if not raw:
        raise ValueError("Player name cannot be empty")

    parts = raw.lower().split()

    # 1) If user typed full name, search by LAST name first (best results)
    if len(parts) >= 2:
        first = parts[0]
        last = parts[-1]

        results = _api_search(last)
        # pick the best match that contains both first and last
        for p in results:
            full = f'{p.get("first_name","")} {p.get("last_name","")}'.lower()
            if first in full and last in full:
                return p

        # fallback: try first name search
        results = _api_search(first)
        for p in results:
            full = f'{p.get("first_name","")} {p.get("last_name","")}'.lower()
            if first in full and last in full:
                return p

        raise ValueError(f"No player found for '{raw}'")

    # 2) If user typed one word, normal search
    results = _api_search(raw)
    if not results:
        raise ValueError(f"No player found for '{raw}'")

    return results[0]
