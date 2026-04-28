from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import datetime

app = FastAPI()

# -----------------------------
# CORS (frontend autorisé)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# API KEY OpenWeather
# -----------------------------
API_KEY = "10c1922ab8a7f9c05e04fecc0374730b"

# -----------------------------
# HISTORIQUE DES RECHERCHES
# -----------------------------
historique = []
favoris = []

# -----------------------------
# ROUTE RACINE (sert le frontend)
# -----------------------------
@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")

# -----------------------------
# ROUTE HISTORIQUE
# -----------------------------
@app.get("/historique")
def get_historique():
    return {"historique": historique}

# -----------------------------
# ROUTE FAVORIS
# -----------------------------
@app.get("/favoris")
def get_favoris():
    return {"favoris": favoris}

@app.post("/favoris/{ville}")
def add_favori(ville: str):
    if ville not in favoris:
        favoris.append(ville)
    return {"message": "Ville ajoutée aux favoris"}

@app.delete("/favoris/{ville}")
def remove_favori(ville: str):
    if ville in favoris:
        favoris.remove(ville)
    return {"message": "Ville retirée des favoris"}

# -----------------------------
# ROUTE PRÉVISIONS 5 JOURS
# -----------------------------
@app.get("/previsions/{ville}")
def previsions(ville: str):
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={ville}&appid={API_KEY}&units=metric"

        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return {"error": "Ville introuvable ou API error"}

        data = response.json()

        # Grouper par jour (API retourne toutes les 3h)
        jours = {}
        for item in data["list"][:40]:  # 5 jours * 8 mesures = 40
            date = item["dt_txt"].split(" ")[0]  # YYYY-MM-DD
            if date not in jours:
                jours[date] = {
                    "date": date,
                    "temperatures": [],
                    "descriptions": []
                }
            jours[date]["temperatures"].append(item["main"]["temp"])
            jours[date]["descriptions"].append(item["weather"][0]["description"])

        # Calculer moyennes par jour
        previsions_list = []
        for date, info in list(jours.items())[:5]:  # 5 premiers jours
            temp_moy = sum(info["temperatures"]) / len(info["temperatures"])
            desc_freq = max(set(info["descriptions"]), key=info["descriptions"].count)
            previsions_list.append({
                "date": date,
                "temperature_moy": round(temp_moy, 1),
                "description": desc_freq
            })

        return {
            "ville": data["city"]["name"],
            "previsions": previsions_list
        }

    except requests.exceptions.Timeout:
        return {"error": "Timeout API météo"}

    except Exception as e:
        return {"error": str(e)}

# -----------------------------
# ROUTE MÉTÉO
# -----------------------------
@app.get("/meteo/{ville}")
def meteo(ville: str):

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={ville}&appid={API_KEY}&units=metric"

        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return {"error": "Ville introuvable ou API error"}

        data = response.json()

        # 🔥 AJOUT HISTORIQUE ICI
        historique.append(ville)

        # Convertir les timestamps Unix en heures lisibles
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
        sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")

        return {
            "ville": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidite": data["main"]["humidity"],
            "vent": data["wind"]["speed"],
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"],
            "sunrise": sunrise,
            "sunset": sunset
        }

    except requests.exceptions.Timeout:
        return {"error": "Timeout API météo"}

    except Exception as e:
        return {"error": str(e)}

# -----------------------------
# ROUTE MÉTÉO PAR COORDONNÉES
# -----------------------------
@app.get("/meteo/coords/{lat}/{lon}")
def meteo_coords(lat: float, lon: float):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return {"error": "Coordonnées invalides ou API error"}

        data = response.json()

        # 🔥 AJOUT HISTORIQUE ICI
        historique.append(data["name"])

        # Convertir les timestamps Unix en heures lisibles
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
        sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")

        return {
            "ville": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidite": data["main"]["humidity"],
            "vent": data["wind"]["speed"],
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"],
            "sunrise": sunrise,
            "sunset": sunset
        }

    except requests.exceptions.Timeout:
        return {"error": "Timeout API météo"}

    except Exception as e:
        return {"error": str(e)}

# -----------------------------
# ROUTE QUALITÉ DE L'AIR
# -----------------------------
@app.get("/air_quality/{lat}/{lon}")
def air_quality(lat: float, lon: float):
    try:
        url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return {"error": "Erreur récupération qualité de l'air"}

        data = response.json()

        # Extraire les données principales
        aqi = data["list"][0]["main"]["aqi"]  # 1-5 scale
        components = data["list"][0]["components"]

        # Interprétation AQI
        aqi_labels = {
            1: "Bonne",
            2: "Acceptable",
            3: "Modérée",
            4: "Mauvaise",
            5: "Très mauvaise"
        }

        return {
            "aqi": aqi,
            "label": aqi_labels.get(aqi, "Inconnue"),
            "components": {
                "co": components["co"],  # Monoxyde de carbone
                "no": components["no"],  # Monoxyde d'azote
                "no2": components["no2"],  # Dioxyde d'azote
                "o3": components["o3"],  # Ozone
                "so2": components["so2"],  # Dioxyde de soufre
                "pm2_5": components["pm2_5"],  # Particules fines
                "pm10": components["pm10"],  # Particules grossières
                "nh3": components["nh3"]  # Ammoniac
            }
        }

    except requests.exceptions.Timeout:
        return {"error": "Timeout API qualité de l'air"}

    except Exception as e:
        return {"error": str(e)}