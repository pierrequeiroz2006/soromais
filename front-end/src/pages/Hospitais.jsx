import TopAppBar from '../components/TopAppBar'
import BottomNav from '../components/BottomNav'
import HospitalCard from '../components/HospitalCard'
import { useHospitais } from '../context/HospitaisContext'

export default function Hospitais() {
  const { hospitais, loading, geoStatus, requestLocation } = useHospitais()

  return (
    <>
      <TopAppBar />

      <main className="mt-16 px-container-margin max-w-lg mx-auto pb-32">
        
        <section className="mb-lg mt-lg">
          <h2 className="text-[32px] font-extrabold text-on-surface leading-tight">
            Hospitais Próximos
          </h2>
          <p className="text-on-surface-variant font-medium mt-1">
            Hospitais com estoque confirmado de soro antiofídico.
          </p>
          {/* Banner emergência crítica */}
          <div className="mt-xl p-md bg-error-container rounded-xl flex items-start gap-md border-2 border-error/20">
            <span className="material-symbols-outlined text-error text-[40px] shrink-0">
              emergency_home
            </span>
            <div>
              <h4 className="font-extrabold text-on-error-container text-lg">Emergência Crítica?</h4>
              <p className="text-on-error-container font-medium mt-1 text-sm leading-relaxed">
                Se a vítima estiver inconsciente, ligue para o{' '}
                <a href="tel:192" className="font-bold underline">192</a> imediatamente.
              </p>
            </div>
          </div>
        </section>
        {geoStatus === 'loading' && (
          <p className="text-on-surface-variant font-medium animate-pulse">Buscando localização...</p>
        )}

        {geoStatus === 'denied' && (
          <div className="text-error font-medium space-y-1">
            <p>Permissão de localização negada. Ative a localização para este site nas configurações do navegador.</p>
            <button
              type="button"
              onClick={requestLocation}
              className="text-primary font-semibold underline"
            >
              Tentar novamente
            </button>
          </div>
        )}

        {loading && geoStatus === 'granted' && (
          <p className="text-on-surface-variant font-medium animate-pulse">Buscando hospitais...</p>
        )}

        <div className="space-y-6">
          {hospitais.map((hospital, index) => (
            <HospitalCard
              key={hospital.cnes}
              hospital={hospital}
              featured={index === 0}
            />
          ))}
        </div>
      </main>

      <BottomNav />
    </>
  )
}
