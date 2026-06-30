import { useState } from 'react'

const NAO_FAZER = [
  { title: "Não faça torniquete", detail: "pode causar necrose e levar à amputação." },
  { title: "Não corte", detail: "ou faça incisões no local da picada." },
  { title: "Não tente sugar", detail: "o veneno com a boca." },
  { title: "Não aplique remédios caseiros", detail: "(álcool, querosene, folhas, terra, café, etc.)." },
]

const O_QUE_FAZER = [
  { text: "Mantenha a pessoa", bold: "calma e imóvel" },
  { text: "Tire anéis, pulseiras, relógio e roupas apertadas" },
  { text: "Mantenha o local da picada na", bold: "altura do coração" },
  { text: "Lave o local com", bold: "água e sabão" },
]

export default function TopAppBar({ showAlert = true }) {
  const [alertOpen, setAlertOpen] = useState(false)

  return (
    <>
      <header className="bg-surface fixed top-0 w-full z-50 flex justify-between items-center px-container-margin h-14 border-b border-outline-variant">
        <div className="flex items-center gap-xs">
          <span className="material-symbols-outlined text-primary">medical_services</span>
          <h1 className="font-headline-sm text-headline-sm text-primary">Soromais</h1>
        </div>

        {showAlert && (
          <div className="relative flex items-center justify-center">
            <span className="absolute inset-0 rounded-xl bg-error animate-ping opacity-50 pointer-events-none" />
            <button
              onClick={() => setAlertOpen(true)}
              className="relative z-10 w-10 h-10 bg-error rounded-xl flex items-center justify-center active:scale-95 transition-transform"
            >
              <span className="material-symbols-outlined text-white text-[22px]">warning</span>
            </button>
          </div>
        )}
      </header>

      {alertOpen && (
        <div className="fixed inset-0 z-[100] flex flex-col justify-end">
          <div className="absolute inset-0 bg-black/40" onClick={() => setAlertOpen(false)} />

          <div className="relative bg-surface rounded-t-2xl max-h-[85vh] overflow-y-auto">
            <div className="flex justify-center pt-3 pb-1">
              <div className="w-10 h-1 rounded-full bg-outline-variant" />
            </div>

            <div className="flex items-center justify-between px-container-margin py-3 border-b border-outline-variant">
              <h2 className="font-headline-sm text-headline-sm text-on-surface">Alertas de Emergência</h2>
              <button onClick={() => setAlertOpen(false)} className="material-symbols-outlined text-on-surface-variant">
                close
              </button>
            </div>

            <div className="px-container-margin py-md space-y-md pb-10">

              <section className="rounded-xl overflow-hidden border border-outline-variant">
                <div className="bg-error p-4 flex items-center justify-center gap-3 text-white">
                  <span className="material-symbols-outlined">warning</span>
                  <h3 className="font-headline-sm uppercase tracking-wider font-extrabold">O QUE NÃO FAZER</h3>
                </div>
                <ul className="p-4 space-y-3">
                  {NAO_FAZER.map(({ title, detail }) => (
                    <li key={title} className="flex gap-3 items-start">
                      <span className="material-symbols-outlined text-error shrink-0 mt-0.5">cancel</span>
                      <p className="font-body-md text-on-surface">
                        <strong className="font-bold">{title}</strong>
                        {detail ? ` — ${detail}` : ''}
                      </p>
                    </li>
                  ))}
                </ul>
              </section>

              <section className="rounded-xl overflow-hidden border border-outline-variant">
                <div className="bg-primary p-4 flex items-center justify-center gap-3 text-white">
                  <span className="material-symbols-outlined">check_circle</span>
                  <h3 className="font-headline-sm uppercase tracking-wider font-extrabold">O QUE FAZER</h3>
                </div>
                <div className="p-4 space-y-4">
                  <a
                    href="tel:192"
                    className="flex items-center justify-between w-full bg-primary text-white rounded-xl px-4 py-3 active:scale-95 transition-transform"
                  >
                    <div className="flex items-center gap-3">
                      <span className="material-symbols-outlined">call</span>
                      <span className="font-semibold">Ligue para o SAMU: 192</span>
                    </div>
                    <span className="material-symbols-outlined">arrow_forward</span>
                  </a>
                  <ul className="space-y-3">
                    {O_QUE_FAZER.map(({ text, bold }, i) => (
                      <li key={i} className="flex gap-3 items-start">
                        <span className="material-symbols-outlined text-primary shrink-0 mt-0.5">check_circle</span>
                        <p className="font-body-md text-on-surface">
                          {text}{' '}
                          {bold && <strong className="font-bold text-primary">{bold}</strong>}
                        </p>
                      </li>
                    ))}
                  </ul>
                </div>
              </section>

            </div>
          </div>
        </div>
      )}
    </>
  )
}
