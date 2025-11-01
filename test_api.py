import requests

API_KEY = "f50c3bb69922405b8963e15c66c23877"  # tu token personal
HEADERS = {"X-Auth-Token": API_KEY}

# Probamos con la Premier League (código PL)
url = "https://api.football-data.org/v4/competitions/PL/standings"

resp = requests.get(url, headers=HEADERS)
print("Status:", resp.status_code)

if resp.status_code == 200:
    data = resp.json()
    table = data["standings"][0]["table"]
    print("Primeros 3 equipos de la Premier League:")
    for row in table[:3]:
        print(f"{row['team']['name']} - {row['points']} pts")
else:
    print("Error:", resp.text)
