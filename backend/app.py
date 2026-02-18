from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    return {
        "player1": player1,
        "player2": player2,
        "decision": "comparison logic coming soon",
        "explanation": "Backend working successfully"
    }
