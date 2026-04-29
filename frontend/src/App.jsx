import { useState } from "react";
import "./App.css";

function App() {
  const [ville, setVille] = useState("");
  const [meteo, setMeteo] = useState(null);
  const [previsions, setPrevisions] = useState([]);
  const [favoris, setFavoris] = useState([]);
  const [historique, setHistorique] = useState([]);
  const [air, setAir] = useState(null);
  const [showFavoris, setShowFavoris] = useState(false);
  const [showHistorique, setShowHistorique] = useState(false);

  // 🎨 BACKGROUND
  const getBackground = () => {
    if (!meteo) return "default";
    const desc = meteo.description.toLowerCase();

    if (desc.includes("rain")) return "rain";
    if (desc.includes("cloud")) return "cloud";
    if (desc.includes("clear")) return "sun";
    return "default";
  };

  const getMeteo = async (villeParam = ville) => {
  const res = await fetch(`http://127.0.0.1:8000/meteo/${villeParam}`);
  const data = await res.json();

  if (data.error) return alert(data.error);

  setMeteo(data);
  setVille(villeParam);

  // 🔥 RESET PREVISIONS (IMPORTANT)
  setPrevisions([]);

  const airRes = await fetch(
    `http://127.0.0.1:8000/air_quality/${data.lat}/${data.lon}`
  );
  const airData = await airRes.json();
  setAir(airData);
};

  const getPrevisions = async () => {
    const res = await fetch(`http://127.0.0.1:8000/previsions/${ville}`);
    const data = await res.json();
    setPrevisions(data.previsions || []);
  };

  const loadFavoris = async () => {
    const res = await fetch(`http://127.0.0.1:8000/favoris`);
    const data = await res.json();
    setFavoris(data.favoris);
  };

  const loadHistorique = async () => {
    const res = await fetch(`http://127.0.0.1:8000/historique`);
    const data = await res.json();
    setHistorique(data.historique);
  };

  const addFavori = async () => {
    await fetch(`http://127.0.0.1:8000/favoris/${ville}`, {
      method: "POST",
    });
    loadFavoris();
  };

  return (
    <div className={`app ${getBackground()}`}>
      <div className="overlay"></div>

      {/* 🔝 TOP RIGHT */}
      <div className="top-bar">
        <button
          onClick={() => {
            loadFavoris();
            setShowFavoris(true);
            setShowHistorique(false);
          }}
        >
          ⭐
        </button>

        <button
          onClick={() => {
            loadHistorique();
            setShowHistorique(true);
            setShowFavoris(false);
          }}
        >
          🕓
        </button>
      </div>

      <div className="container">
        <h1 className="title">🌤️ Weather App</h1>

        {/* SEARCH */}
        <div className="search-box">
          <input
            value={ville}
            onChange={(e) => setVille(e.target.value)}
            placeholder="Entrer une ville..."
          />
          <button onClick={() => getMeteo()}>Météo</button>
          <button onClick={getPrevisions}>Prévisions</button>
          <button onClick={addFavori}>⭐</button>
        </div>

        {/* METEO */}
        
        {meteo && (
          
          <div className="card meteo-card">
            <h2>{meteo.ville}</h2>
            <h1 className="temp">{meteo.temperature}°C</h1>
            <p className="desc">{meteo.description}</p>

            <div className="grid">
              <span>💧 {meteo.humidite}%</span>
              <span>💨 {meteo.vent} m/s</span>
              <span>🌅 {meteo.sunrise}</span>
              <span>🌇 {meteo.sunset}</span>
            </div>
          </div>
        )}

        {/* AIR */}
        {air && (
          <div className="card">
            <h3>🌍 Qualité de l’air</h3>
            <p>{air.label}</p>
            <p>PM2.5: {air.components.pm2_5}</p>
          </div>
        )}

        {/* PREVISIONS */}
        {previsions.length > 0 && (
          <div className="card">
            <h3>📊 Prévisions</h3>
            <div className="previsions">
              {previsions.map((p, i) => (
                <div key={i} className="mini-card">
                  <p>{p.date}</p>
                  <p>{p.temperature_moy}°C</p>
                  <p>{p.description}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* ⭐ PANEL FAVORIS */}
      <div className={`side-panel ${showFavoris ? "open" : ""}`}>
        <div className="panel-header">
          <h3>⭐ Favoris</h3>
          <button onClick={() => setShowFavoris(false)}>✖</button>
        </div>

        {favoris.map((f, i) => (
          <p
            key={i}
            onClick={() => {
              getMeteo(f);
              setShowFavoris(false);
            }}
          >
            {f}
          </p>
        ))}
      </div>

      {/* 🕓 PANEL HISTORIQUE */}
      <div className={`side-panel ${showHistorique ? "open" : ""}`}>
        <div className="panel-header">
          <h3>🕓 Historique</h3>
          <button onClick={() => setShowHistorique(false)}>✖</button>
        </div>

        {historique.map((h, i) => (
          <p
            key={i}
            onClick={() => {
              getMeteo(h);
              setShowHistorique(false);
            }}
          >
            {h}
          </p>
        ))}
      </div>
    </div>
  );
}

export default App;