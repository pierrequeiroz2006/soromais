import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Identificar from './pages/Identificar'
import Hospitais from './pages/Hospitais'
import Relatorio from './pages/Relatorio'
import { useGeolocation } from './hooks/useGeolocation'

export default function App() {
  const { status, coords } = useGeolocation()

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Identificar />} />
        <Route path="/hospitais" element={<Hospitais />} />
        <Route path="/relatorio" element={<Relatorio />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  )
}