import TopAppBar from '../components/TopAppBar'
import BottomNav from '../components/BottomNav'
import HospitalCard from '../components/HospitalCard'

const HOSPITALS = [
  {
    id: 1,
    nome: 'Hospital Central de Emergência',
    endereco: 'Rua das Flores, 120 - Centro',
    distancia: '1.2 km',
    tempo: '4 min',
    telefone: '192',
  },
  {
    id: 2,
    nome: 'Pronto Socorro São Lucas',
    endereco: 'Av. Paulista, 1500 - Bela Vista',
    distancia: '2.8 km',
    tempo: '8 min',
    telefone: '192',
  },
  {
    id: 3,
    nome: 'Clínica Geral Norte',
    endereco: 'Rua do Comércio, 45 - Norte',
    distancia: '4.5 km',
    tempo: '12 min',
    telefone: '192',
  },
  {
    id: 4,
    nome: 'Hospital Municipal Sul',
    endereco: 'Alameda dos Anjos, 900 - Sul',
    distancia: '5.1 km',
    tempo: '15 min',
    telefone: '192',
  },
  {
    id: 5,
    nome: 'Unidade de Saúde Leste',
    endereco: 'Travessa da Paz, 12 - Leste',
    distancia: '6.7 km',
    tempo: '20 min',
    telefone: '192',
  },
]

export default function Hospitais() {
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
        </section>

        <div className="space-y-6">
          {HOSPITALS.map((hospital, index) => (
            <HospitalCard
              key={hospital.id}
              hospital={hospital}
              featured={index === 0}
            />
          ))}
        </div>

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
      </main>

      <BottomNav />
    </>
  )
}
