import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Identificar from './pages/Identificar'
import Hospitais from './pages/Hospitais'
import Relatorio from './pages/Relatorio'
import { HospitaisProvider } from './context/HospitaisContext'
import { GeolocalizacaoProvider } from './context/GeolocalizacaoContext'

export default function App() {
  return (
    <BrowserRouter>
      <GeolocalizacaoProvider>
        <HospitaisProvider>
          <Routes>
          <Route path="/" element={<Identificar />} />
          <Route path="/hospitais" element={<Hospitais />} />
          <Route path="/relatorio" element={<Relatorio />} />
          <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </HospitaisProvider>
      </GeolocalizacaoProvider>
    </BrowserRouter>
  )
}