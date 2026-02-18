from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.services.balldontlie import search_player, get_todays_opponent


app = FastAPI(title="Fantasy Start/Sit API")

# allow frontend to talk to backend (important later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Fantasy Start/Sit API is running"}


@app.get("/compare")
def compare(player1: str, player2: str):
    """
    Compare two players by looking them up from NBA API.
    """

    try:
        p1 = search_player(player1)
        p2 = search_player(player2)
        
        opp1 = get_todays_opponent(p1["team"]["id"])
        opp2 = get_todays_opponent(p2["team"]["id"])

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
    "player1_found": {
        "name": f'{p1["first_name"]} {p1["last_name"]}',
        "team": p1["team"]["full_name"],
        "opponent_today": opp1["full_name"] if opp1 else None,
    },
    "player2_found": {
        "name": f'{p2["first_name"]} {p2["last_name"]}',
        "team": p2["team"]["full_name"],
        "opponent_today": opp2["full_name"] if opp2 else None,
    },
    "next": "use opponent defense vs position to pick start/sit"
}

