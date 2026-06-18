import { createContext, useContext } from 'react'
import { useGeolocation } from '../hooks/useGeolocation'

const GeolocalizacaoContext = createContext(null)

export function GeolocalizacaoProvider({ children }) {
  const value = useGeolocation()
  return <GeolocalizacaoContext.Provider value={value}>{children}</GeolocalizacaoContext.Provider>
}

export function useGeolocalizacao() {
  return useContext(GeolocalizacaoContext)
}
