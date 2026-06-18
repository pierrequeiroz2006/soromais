import { useState, useEffect } from 'react'
import { useGeolocalizacao } from '../context/GeolocalizacaoContext'

const API_URL = import.meta.env.VITE_API_URL

export function useHospitaisProximos() {
  const { coords, status: geoStatus } = useGeolocalizacao()
  const [hospitais, setHospitais] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (geoStatus !== 'granted' || !coords) return

    setLoading(true)
    fetch(`${API_URL}/hospitais/proximos?lat=${coords.latitude}&lng=${coords.longitude}`)
      .then(res => res.json())
      .then(data => setHospitais(data))
      .catch(err => setError(err))
      .finally(() => setLoading(false))
  }, [coords, geoStatus])

  return { hospitais, loading, error, geoStatus }
}
