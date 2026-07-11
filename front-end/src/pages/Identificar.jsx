import { useNavigate } from 'react-router-dom'
import TopAppBar from '../components/TopAppBar'
import BottomNav from '../components/BottomNav'

const NAO_FAZER = [
  {
    title: "Não faça torniquete",
    detail: "pode causar necrose e levar à amputação.",
  },
  {
    title: "Não corte",
    detail: "ou faça incisões no local da picada.",
  },
  {
    title: "Não tente sugar",
    detail: "o veneno com a boca.",
  },
  {
    title: "Não aplique remédios caseiros",
    detail: "(álcool, querosene, folhas, terra, café, etc.).",
  },
];

const O_QUE_FAZER = [
  { text: "Mantenha a pessoa", bold: "calma e imóvel" },
  { text: "Tire anéis, pulseiras, relógio e roupas apertadas" },
  { text: "Mantenha o local da picada na", bold: "altura do coração" },
  { text: "Lave o local com", bold: "água e sabão" },
];

// ── Material Symbol component ──────────────────────────────────
function Icon({ name, className = "" }) {
  return (
    <span
      className={`material-symbols-outlined ${className}`}
      style={{ fontVariationSettings: "'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24" }}
    >
      {name}
    </span>
  );
}

// ── Main page ─────────────────────────────────────────────────
export default function PrimeirosSocorros() {
  const navigate = useNavigate()

  return (
    <>
      <TopAppBar />

      <main className="mt-14 mb-20 px-4 py-6 overflow-y-auto">
        <div className="max-w-xl mx-auto space-y-6">

          {/* Identify animal button */}
          <div onClick={() => navigate('/relatorio')} className="w-full rounded-lg flex flex-col items-center justify-center gap-3 shadow-md transition-transform active:scale-95 cursor-pointer bg-primary px-6 py-4">
            <Icon name="photo_camera" className="text-white text-3xl" />
            <h3 className="font-headline-sm text-white uppercase tracking-wider font-extrabold text-center">
              IDENTIFIQUE O ANIMAL
            </h3>
          </div>

          {/* ── O QUE NÃO FAZER ── */}
          <section className="relative overflow-hidden rounded-xl border border-outline-variant bg-surface-bright shadow-sm">
            <div className="bg-error p-4 flex items-center justify-center gap-3 text-white">
              <Icon name="warning" className="text-3xl" />
              <h2 className="font-headline-sm text-headline-sm uppercase tracking-wider font-extrabold">
                O QUE NÃO FAZER
              </h2>
            </div>
            <div className="p-6">
              <ul className="space-y-4">
                {NAO_FAZER.map(({ title, detail }) => (
                  <li key={title} className="flex gap-4 items-start">
                    <Icon name="cancel" className="text-error shrink-0 mt-0.5" />
                    <p className="font-body-lg text-body-lg leading-tight text-on-surface">
                      <strong className="font-bold">{title}</strong>
                      {detail ? ` — ${detail}` : ""}
                    </p>
                  </li>
                ))}
              </ul>
            </div>
          </section>

          {/* ── O QUE FAZER ── */}
          <section className="relative overflow-hidden rounded-xl border border-outline-variant bg-surface-bright shadow-sm">
            <div className="bg-primary p-4 flex items-center justify-center gap-3 text-white">
              <Icon name="check_circle" className="text-3xl" />
              <h2 className="font-headline-sm text-headline-sm uppercase tracking-wider font-extrabold">
                O QUE FAZER
              </h2>
            </div>
            <div className="p-6 space-y-6">

              {/* Emergency call */}
              <a
                href="tel:192"
                className="flex items-center justify-between w-full bg-primary text-white rounded-xl shadow-md active:scale-95 transition-transform px-4 py-3"
                onClick={() => console.log("Initiating emergency call...")}
              >
                <div className="flex items-center gap-4">
                  <Icon name="call" className="text-3xl" />
                  <div className="text-left">
                    <p className="font-headline-md text-headline-md leading-none">
                      Ligue para o SAMU: 192
                    </p>
                  </div>
                </div>
                <Icon name="arrow_forward" />
              </a>

              {/* Steps */}
              <ul className="space-y-4">
                {O_QUE_FAZER.map(({ text, bold }, i) => (
                  <li key={i} className="flex gap-4 items-start">
                    <Icon name="check_circle" className="text-primary shrink-0 mt-0.5" />
                    <p className="font-body-lg text-body-lg leading-tight text-on-surface">
                      {text}{" "}
                      {bold && (
                        <strong className="font-bold text-primary">{bold}</strong>
                      )}
                    </p>
                  </li>
                ))}
              </ul>

              {/* Hospital alert */}
              <div onClick={() => navigate('/hospitais')} className="flex items-start gap-4 p-4 rounded-lg bg-primary-container text-on-primary-container cursor-pointer active:scale-95 transition-transform">
                <Icon name="local_hospital" />
                <p className="font-body-lg text-body-lg font-bold">
                  Leve ao hospital o mais rápido possível
                </p>
              </div>

            </div>
          </section>

        </div>
      </main>

      <BottomNav />
    </>
  );
}