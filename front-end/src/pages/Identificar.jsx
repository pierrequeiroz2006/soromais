import TopAppBar from '../components/TopAppBar'
import BottomNav from '../components/BottomNav'

export default function Identificar() {
  return (
    <>
      <TopAppBar />
      <main className="pt-14 px-container-margin max-w-[800px] mx-auto pb-32">
        <section className="mt-lg flex flex-col items-center justify-center gap-md text-center py-xl">
          <span className="material-symbols-outlined text-primary text-6xl">photo_camera</span>
          <h2 className="font-headline-md text-headline-md text-on-surface">
            Identificar Animal
          </h2>
          <p className="font-body-md text-body-md text-on-surface-variant">
            Em breve — integração com Gemini Vision
          </p>
        </section>
      </main>
      <BottomNav />
    </>
  )
}
