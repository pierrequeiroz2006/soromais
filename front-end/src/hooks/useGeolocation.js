import { useState, useEffect } from "react";

export function useGeolocation() {
  const [status, setStatus] = useState("idle");
  const [coords, setCoords] = useState(null);

  useEffect(() => {
    console.log("[geo] hook iniciado");

    if (!navigator.geolocation) {
      console.warn("[geo] navigator.geolocation não disponível");
      setStatus("error");
      return;
    }

    setStatus("loading");
    console.log("[geo] solicitando permissão...");

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        console.log("[geo] ✅ coordenadas:", { latitude, longitude });
        setCoords({ latitude, longitude });
        setStatus("granted");
      },
      (err) => {
        console.warn("[geo] ❌ erro/negado:", err.code, err.message);
        setStatus("denied");
      },
      { enableHighAccuracy: false, timeout: 30_000 }
    );
  }, []);

  return { status, coords };
}

//FUNCIONANDO APENAS EM LOCALHOST, APENAS QUANDO FOR PARA PRODUÇÃO IRÁ FUNCIONAR