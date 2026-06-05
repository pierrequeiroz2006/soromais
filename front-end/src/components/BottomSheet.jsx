import { useEffect } from 'react'
import HospitalCard from './HospitalCard'

const SHEET_HOSPITALS = [
  { id: 1, nome: 'HU - Hospital Universitário', distancia: null, telefone: '192' },
  { id: 2, nome: 'Hospital Municipal de Emergência', distancia: '1.2 km', telefone: '192' },
  { id: 3, nome: 'Santa Casa de Misericórdia', distancia: '2.5 km', telefone: '192' },
  { id: 4, nome: 'Hospital Regional', distancia: '4.1 km', telefone: '192' },
]

export default function BottomSheet({ open, onClose }) {
  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : ''
    return () => { document.body.style.overflow = '' }
  }, [open])

  return (
    <>
      {/* Overlay */}
      <div
        onClick={onClose}
        className={`fixed inset-0 bg-black/40 z-[60] transition-opacity duration-300
          ${open ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'}`}
      />

      {/* Sheet */}
      <div className={`fixed bottom-0 left-0 right-0 z-[70] max-w-[800px] mx-auto bg-surface
        rounded-t-[32px] shadow-2xl border-t border-outline-variant
        transform transition-transform duration-300
        ${open ? 'translate-y-0' : 'translate-y-full'}`}
      >
        <div className="flex flex-col p-container-margin">
          {/* Handle */}
          <button
            onClick={onClose}
            className="w-12 h-1.5 bg-outline-variant rounded-full self-center mb-md"
            aria-label="Fechar"
          />

          <div className="flex items-center gap-sm mb-lg">
            <span className="material-symbols-outlined text-primary text-2xl">send</span>
            <h2 className="font-headline-md text-headline-md text-on-surface">
              Enviar para Hospital
            </h2>
          </div>

          <div className="space-y-md pb-xl">
            {SHEET_HOSPITALS.map((h, i) => (
              <HospitalCard key={h.id} hospital={h} featured={i === 0} variant="sheet" />
            ))}
          </div>
        </div>
      </div>
    </>
  )
}
