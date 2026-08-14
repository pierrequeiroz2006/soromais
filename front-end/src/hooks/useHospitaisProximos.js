import { useState, useEffect } from 'react'
import { useGeolocalizacao } from '../context/GeolocalizacaoContext'
import { apiFetch } from '../api'

export function useHospitaisProximos() {
  const { coords, status: geoStatus, requestLocation, canRetry } = useGeolocalizacao()
  const [hospitais, setHospitais] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (geoStatus !== 'granted' || !coords) return

    setLoading(true)
    apiFetch(`/hospitais/proximos?lat=${coords.latitude}&lng=${coords.longitude}`)
      .then(res => res.json())
      .then(data => setHospitais(data))
      .catch(err => setError(err))
      .finally(() => setLoading(false))
  }, [coords, geoStatus])

  return { hospitais, loading, error, geoStatus, requestLocation, canRetry }
}
