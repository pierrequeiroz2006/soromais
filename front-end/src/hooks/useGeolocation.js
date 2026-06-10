import { useState, useEffect } from "react";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export function useGeolocation() {
  const [status, setStatus] = useState("idle"); // idle | loading | granted | denied | error
  const [coords, setCoords] = useState(null);

  useEffect(() => {
    if (!navigator.geolocation) {
      setStatus("error");
      return;
    }

    setStatus("loading");

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        setCoords({ latitude, longitude });
        setStatus("granted");

        try {
          await fetch(`${API_BASE}/api/localizacao`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ latitude, longitude }),
          });
        } catch (err) {
          console.error("Erro ao enviar localização:", err);
        }
      },
      (err) => {
        console.warn("Permissão de localização negada:", err.message);
        setStatus("denied");
      },
      { enableHighAccuracy: true, timeout: 10_000 }
    );
  }, []);

  return { status, coords };
}