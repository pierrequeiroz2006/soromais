import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Identificar from './pages/Identificar'
import Hospitais from './pages/Hospitais'
import Relatorio from './pages/Relatorio'

export default function App() {
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
