import requests

BASE_URL = "https://www.balldontlie.io/api/v1"


def search_player(name: str):
    """
    Search for NBA player by name.
    Returns the first matching player.
    """
    response = requests.get(
        f"{BASE_URL}/players",
        params={"search": name}
    )

    response.raise_for_status()
    data = response.json()["data"]

    if not data:
        raise ValueError(f"No player found for {name}")

    return data[0]
