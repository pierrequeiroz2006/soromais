import { useState, useEffect, useCallback } from "react";

export function useGeolocation() {
  const [status, setStatus] = useState("idle");
  const [coords, setCoords] = useState(null);
  // "prompt" = navegador ainda pode exibir o popup; "denied" = bloqueado até o
  // usuário reativar manualmente nas configurações do site/navegador.
  const [permissionState, setPermissionState] = useState(null);

  const requestLocation = useCallback(() => {
    if (!navigator.geolocation) {
      console.warn("[geo] navigator.geolocation não disponível");
      setStatus("error");
      return;
    }

    setStatus("loading");

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        setCoords({ latitude, longitude });
        setStatus("granted");
      },
      (err) => {
        console.warn("[geo] erro/negado:", err.code, err.message);
        setStatus(err.code === err.PERMISSION_DENIED ? "denied" : "error");
      },
      { enableHighAccuracy: false, timeout: 30_000 }
    );
  }, []);

  useEffect(() => {
    requestLocation();

    if (!navigator.permissions?.query) return;

    let permissionStatus;
    let cancelled = false;

    const handleChange = () => {
      setPermissionState(permissionStatus.state);
      // Usuário reativou a localização nas configurações: busca de novo
      // automaticamente, sem precisar de um novo clique.
      if (permissionStatus.state === "granted" || permissionStatus.state === "prompt") {
        requestLocation();
      }
    };

    navigator.permissions.query({ name: "geolocation" }).then((result) => {
      if (cancelled) return;
      permissionStatus = result;
      setPermissionState(permissionStatus.state);
      permissionStatus.addEventListener("change", handleChange);
    }).catch(() => {});

    return () => {
      cancelled = true;
      permissionStatus?.removeEventListener("change", handleChange);
    };
  }, [requestLocation]);

  // Só faz sentido oferecer "tentar novamente": quando ainda não há decisão
  // salva, ou quando o navegador não expõe a Permissions API (ex.: Safari).
  const canRetry = permissionState !== "denied";

  return { status, coords, requestLocation, canRetry };
}

//FUNCIONANDO APENAS EM LOCALHOST, APENAS QUANDO FOR PARA PRODUÇÃO IRÁ FUNCIONAR