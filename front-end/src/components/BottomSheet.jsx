import { useEffect } from 'react'
import HospitalCard from './HospitalCard'
import { useHospitais } from '../context/HospitaisContext'

export default function BottomSheet({ open, onClose, dadosRelatorio }) {
  const { hospitais, loading } = useHospitais()

  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : ''
    return () => { document.body.style.overflow = '' }
  }, [open])

  return (
    <>
      <div
        onClick={onClose}
        className={`fixed inset-0 bg-black/40 z-[60] transition-opacity duration-300
          ${open ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'}`}
      />
      <div className={`fixed bottom-0 left-0 right-0 z-[70] max-w-[800px] mx-auto bg-surface
        rounded-t-[32px] shadow-2xl border-t border-outline-variant
        transform transition-transform duration-300
        ${open ? 'translate-y-0' : 'translate-y-full'}`}
      >
        <div className="flex flex-col p-container-margin max-h-[80vh] overflow-y-auto">
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
            {loading && (
              <p className="text-on-surface-variant text-sm">Buscando hospitais próximos...</p>
            )}
            {!loading && hospitais.length === 0 && (
              <p className="text-on-surface-variant text-sm">Nenhum hospital encontrado próximo a você.</p>
            )}
            {hospitais.map((h, i) => (
              <HospitalCard
                key={h.id}
                hospital={h}
                featured={i === 0}
                variant="sheet"
                dadosRelatorio={dadosRelatorio}
                onEnviado={onClose}
              />
            ))}
          </div>
        </div>
      </div>
    </>
  )
}
