import os
from datetime import date, timedelta

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
    raw = name.strip()
    if not raw:
        raise ValueError("Player name cannot be empty")

    parts = raw.lower().split()

    # Full name: search by last name first
    if len(parts) >= 2:
        first = parts[0]
        last = parts[-1]

        results = _api_search(last)
        for p in results:
            full = f'{p.get("first_name","")} {p.get("last_name","")}'.lower()
            if first in full and last in full:
                return p

        results = _api_search(first)
        for p in results:
            full = f'{p.get("first_name","")} {p.get("last_name","")}'.lower()
            if first in full and last in full:
                return p

        raise ValueError(f"No player found for '{raw}'")

    # One word name
    results = _api_search(raw)
    if not results:
        raise ValueError(f"No player found for '{raw}'")
    return results[0]


from datetime import date, timedelta

def get_next_opponent(team_id: int, days_ahead: int = 7) -> dict | None:
    """
    Finds the opponent for the next game within the next `days_ahead` days.
    Uses ONE API request to avoid rate limits.
    """
    today = date.today()
    dates = [(today + timedelta(days=i)).isoformat() for i in range(days_ahead + 1)]

    # Build repeated dates[] params
    params = [("team_ids[]", team_id), ("per_page", 100)]
    params += [("dates[]", d) for d in dates]

    r = requests.get(
        f"{BASE_URL}/games",
        params=params,
        headers=_headers(),
        timeout=15,
    )
    r.raise_for_status()

    games = r.json().get("data", [])
    if not games:
        return None

    # Sort by date/time just in case API returns unsorted
    games.sort(key=lambda g: g.get("date", ""))

    game = games[0]
    home = game["home_team"]
    away = game["visitor_team"]

    opponent = away if home["id"] == team_id else home

    # game["date"] is usually ISO datetime; keep just YYYY-MM-DD
    game_date = (game.get("date") or "")[:10] or dates[0]

    return {"opponent": opponent, "game_date": game_date}
