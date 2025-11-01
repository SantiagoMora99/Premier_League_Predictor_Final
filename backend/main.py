from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import math
import os
import time

app = FastAPI()

# ====== CONFIG PERSONAL ======
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY", "f50c3bb69922405b8963e15c66c23877")  # permite override por entorno
LEAGUE = "PL"  # Premier League
API_BASE = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}
# =============================

# Permitir que el frontend React pueda comunicarse sin bloqueos CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# CACHÉ SIMPLE
# =============================
_STANDINGS_CACHE = {"data": None, "ts": 0}
_CACHE_TTL_SECONDS = 300  # 5 minutos

# =============================
# FUNCIONES INTERNAS
# =============================

def fetch_standings():
    """Trae la tabla de posiciones actual con caché y manejo de errores."""
    now = time.time()
    if _STANDINGS_CACHE["data"] is not None and (now - _STANDINGS_CACHE["ts"]) < _CACHE_TTL_SECONDS:
        return _STANDINGS_CACHE["data"]

    url = f"{API_BASE}/competitions/{LEAGUE}/standings"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error al conectar con API externa: {e}")
    if r.status_code != 200:
        # Si hay límite 429 pero tenemos caché previo, devolvemos caché aunque esté vieja
        if r.status_code == 429 and _STANDINGS_CACHE["data"] is not None:
            return _STANDINGS_CACHE["data"]
        raise HTTPException(status_code=r.status_code, detail=f"API externa respondió {r.status_code}: {r.text}")
    data = r.json()
    try:
        table = data["standings"][0]["table"]
    except (KeyError, IndexError, TypeError):
        # Si la respuesta es inesperada pero tenemos caché, usamos caché
        if _STANDINGS_CACHE["data"] is not None:
            return _STANDINGS_CACHE["data"]
        raise HTTPException(status_code=502, detail="Respuesta inesperada de la API externa.")

    teams = []
    for row in table:
        teams.append({
            "id": row["team"]["id"],
            "name": row["team"]["name"],
            "played": row["playedGames"],
            "points": row["points"],
            "goalsFor": row["goalsFor"],
            "goalsAgainst": row["goalsAgainst"],
            "won": row["won"],
            "draw": row["draw"],
            "lost": row["lost"],
        })

    # Actualizamos caché
    _STANDINGS_CACHE["data"] = teams
    _STANDINGS_CACHE["ts"] = now
    return teams


def team_score(team):
    """Calcula una puntuación heurística del equipo."""
    pj = max(team["played"], 1)
    ataque = team["goalsFor"] / pj
    defensa = team["goalsAgainst"] / pj
    forma = team["points"] / pj
    defensa_valor = 1 / defensa if defensa > 0 else 1.5
    return ataque * 0.4 + defensa_valor * 0.4 + forma * 0.2


def probabilidad_ganar(teamA, teamB):
    """Convierte los scores en probabilidad tipo softmax binario."""
    sA = team_score(teamA)
    sB = team_score(teamB)
    expA = math.exp(sA)
    expB = math.exp(sB)
    pA = expA / (expA + expB)
    pB = expB / (expA + expB)
    return pA, pB


# =============================
# ENDPOINTS
# =============================

@app.get("/teams")
def get_teams():
    """Devuelve los equipos con stats básicas."""
    teams = fetch_standings()
    return {"league": LEAGUE, "teams": sorted(teams, key=lambda t: t["name"])}


@app.get("/predict")
def predict(teamA_id: int, teamB_id: int):
    """Devuelve la predicción entre dos equipos."""
    teams = fetch_standings()
    if teamA_id == teamB_id:
        raise HTTPException(status_code=400, detail="Debe elegir dos equipos diferentes.")

    try:
        ta = next(t for t in teams if t["id"] == teamA_id)
    except StopIteration:
        raise HTTPException(status_code=404, detail=f"Equipo {teamA_id} no encontrado.")

    try:
        tb = next(t for t in teams if t["id"] == teamB_id)
    except StopIteration:
        raise HTTPException(status_code=404, detail=f"Equipo {teamB_id} no encontrado.")

    pA, pB = probabilidad_ganar(ta, tb)
    winner = ta["name"] if pA > pB else tb["name"]
    confidence = max(pA, pB)

    return {
        "teamA": ta["name"],
        "teamB": tb["name"],
        "probA": round(pA * 100, 2),
        "probB": round(pB * 100, 2),
        "winner": winner,
        "confidence": round(confidence * 100, 2),
        "model_note": "Heurística educativa basada en ataque, defensa y puntos/partido. No es recomendación de apuesta."
    }


@app.get("/health")
def health():
    return {"status": "ok"}
