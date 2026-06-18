import { createContext, useContext } from 'react'
import { useHospitaisProximos } from '../hooks/useHospitaisProximos'

const HospitaisContext = createContext(null)

export function HospitaisProvider({ children }) {
  const value = useHospitaisProximos()
  return <HospitaisContext.Provider value={value}>{children}</HospitaisContext.Provider>
}

export function useHospitais() {
  return useContext(HospitaisContext)
}
