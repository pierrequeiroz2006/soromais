import { useState, useRef } from 'react'
import TopAppBar from '../components/TopAppBar'
import BottomNav from '../components/BottomNav'
import BottomSheet from '../components/BottomSheet'

export default function Relatorio() {
  const [sheetOpen, setSheetOpen] = useState(false)
  const [form, setForm] = useState({
    nome: '', estado: '', localPicada: '',
    tempo: '', peso: '', idade: '',
  })

  const [fotoArquivo, setFotoArquivo] = useState(null)
  const [fotoPreview, setFotoPreview] = useState(null)

  const handleFileChange = (e) => {
    const arquivo = e.target.files[0]
    if (arquivo) {
      setFotoArquivo(arquivo)
      // Cria uma URL temporária para mostrar a foto na tela
      setFotoPreview(URL.createObjectURL(arquivo))

      
    }
  }

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }



  // animal seria preenchido pelo Gemini futuramente
  const animal = null

  return (
    <>
      <TopAppBar />

      <main className="pt-14 px-container-margin space-y-lg max-w-[800px] mx-auto pb-36">

        {/* Foto / Identificação */}
        <section className="mt-lg">
          <div className="high-contrast-card rounded-xl overflow-hidden shadow-sm border border-outline-variant bg-white">
            <input 
            type="file"
            id="fileInput" 
            accept="image/*" 
            onChange={handleFileChange}
            className="hidden" 
            />


            {/* Se a fotoPreview existir, mostra a foto. Se não, mostra o card com o botão */}
            {fotoPreview ? (
              <div className="relative h-64 w-full">
                <img src={fotoPreview} alt="Foto do animal" className="w-full h-full object-cover" />
              </div>
            ) : (
              <div className="h-64 w-full bg-surface-container flex flex-col items-center justify-center gap-sm p-md">
                <span className="material-symbols-outlined text-primary text-5xl">photo_camera</span>
                <h2 className="font-headline-md text-headline-md text-on-surface text-center">
                  Tire ou Envie uma Foto
                </h2>
                <p className="font-body-md text-body-md text-on-surface-variant italic text-center">
                  Identificaremos a espécie automaticamente
                </p>
                
                <label 
                  htmlFor="fileInput" 
                  className="mt-2 border border-primary text-primary px-lg py-2 rounded-lg font-semibold active:scale-95 transition-transform hover:bg-primary/5 cursor-pointer inline-block text-center"
                >
                  Enviar foto
                </label>

                <button className="text-primary px-lg py-2 rounded-lg font-semibold active:scale-95 transition-transform hover:bg-primary/5 underline">
                  Descrever animal manualmente
                </button>
              </div>
            )}
          </div>
        </section>

        {/* Efeitos do Veneno — só aparece se animal identificado */}
        {animal?.efeitos && (
          <section className="bg-error-container/40 border border-error/30 rounded-xl p-md">
            <div className="flex items-center gap-xs mb-sm">
              <span className="material-symbols-outlined text-error">cancel</span>
              <h3 className="font-headline-sm text-headline-sm text-error">Efeitos do Veneno</h3>
            </div>
            <ul className="space-y-1">
              {animal.efeitos.map((e, i) => (
                <li key={i} className="font-body-md text-body-md text-on-error-container flex gap-2">
                  <span>•</span><span>{e}</span>
                </li>
              ))}
            </ul>
          </section>
        )}

        {/* Grid Dados + Localização */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-md">

          {/* Dados da Vítima */}
          <section className="border border-outline-variant bg-white p-md rounded-xl shadow-sm">
            <div className="flex items-center gap-xs mb-sm">
              <span className="material-symbols-outlined text-primary">person</span>
              <h3 className="font-headline-sm text-headline-sm">Dados da Vítima</h3>
            </div>
            <div className="space-y-sm">
              <div>
                <label className="font-label-caps text-label-caps text-on-surface-variant uppercase mb-1 block">
                  TEMPO DECORRIDO
                </label>
                <input
                  name="tempo"
                  value={form.tempo}
                  onChange={handleChange}
                  placeholder="Ex: 45 min"
                  className="w-full bg-surface-container-low border border-outline-variant rounded-lg px-md py-2 font-body-lg text-on-surface focus:border-primary focus:outline-none"
                />
              </div>
              <div>
                <label className="font-label-caps text-label-caps text-on-surface-variant uppercase mb-1 block">
                  LOCAL DA PICADA
                </label>
                <input
                  name="localPicada"
                  value={form.localPicada}
                  onChange={handleChange}
                  placeholder="Ex: Tornozelo direito"
                  className="w-full bg-surface-container-low border border-outline-variant rounded-lg px-md py-2 font-body-lg text-on-surface focus:border-primary focus:outline-none"
                />
              </div>
              <div>
                <label className="font-label-caps text-label-caps text-on-surface-variant uppercase mb-1 block">
                  ESTADO
                </label>
                <input
                  name="estado"
                  value={form.estado}
                  onChange={handleChange}
                  placeholder="Ex: Consciente, dor aguda"
                  className="w-full bg-surface-container-low border border-outline-variant rounded-lg px-md py-2 font-body-lg text-on-surface focus:border-primary focus:outline-none"
                />
              </div>
              <div className="grid grid-cols-3 gap-xs">
                <div>
                  <label className="font-label-caps text-label-caps text-on-surface-variant uppercase mb-1 block">
                    PESO
                  </label>
                  <input
                    name="peso"
                    value={form.peso}
                    onChange={handleChange}
                    placeholder="-- kg"
                    className="w-full bg-surface-container-low border border-outline-variant rounded-lg px-2 py-2 font-body-lg text-on-surface focus:border-primary focus:outline-none"
                  />
                </div>
                <div>
                  <label className="font-label-caps text-label-caps text-on-surface-variant uppercase mb-1 block">
                    IDADE
                  </label>
                  <input
                    name="idade"
                    value={form.idade}
                    onChange={handleChange}
                    placeholder="-- anos"
                    className="w-full bg-surface-container-low border border-outline-variant rounded-lg px-2 py-2 font-body-lg text-on-surface focus:border-primary focus:outline-none"
                  />
                </div>
                <div>
                  <label className="font-label-caps text-label-caps text-on-surface-variant uppercase mb-1 block">
                    NOME
                  </label>
                  <input
                    name="nome"
                    value={form.nome}
                    onChange={handleChange}
                    placeholder="Nome"
                    className="w-full bg-surface-container-low border border-outline-variant rounded-lg px-2 py-2 font-body-lg text-on-surface focus:border-primary focus:outline-none"
                  />
                </div>
              </div>
              <button className="w-full flex items-center justify-center gap-xs bg-primary text-on-primary py-2 rounded-lg font-semibold mt-2 active:scale-95 transition-transform">
                <span className="material-symbols-outlined text-[20px]">save</span>
                Salvar Dados
              </button>
            </div>
          </section>

          {/* Localização */}
          <section className="border border-outline-variant bg-white p-md rounded-xl shadow-sm">
            <div className="flex items-center gap-xs mb-sm">
              <span className="material-symbols-outlined text-primary">location_on</span>
              <h3 className="font-headline-sm text-headline-sm">Localização</h3>
            </div>
            <div className="space-y-sm">
              <div className="h-32 w-full bg-surface-container rounded-lg relative overflow-hidden border border-outline-variant mb-sm">
                <img
                  alt="Localização do acidente"
                  className="w-full h-full object-cover opacity-80"
                  src="https://lh3.googleusercontent.com/aida-public/AB6AXuBT5w71ZMalEMF7eH60U6vWkWdxVr7obAs2Lbtr1ni9lrFrIiYUmzyaD00iz1rUE5LMjjAyRChQsBum_n7y_muc2jo32WC-_ubPu0Epgf7G_-7_mBGZOE7GW-OjMp8W6VWak1JC7fhXj8msXIpjZMJERq_DdBHzHpb5eE0ffCJA_VbV_lkQGTF3b4za6BJUzQ5wp4c3Iqa7ykGT-u_JwmCwEijS0FOC_YzpgPmvE-EW_LSCBIduhkvWvVcH6EK8s1srkQlWnGIVrZld"
                />
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <span
                    className="material-symbols-outlined text-secondary text-3xl"
                    style={{ fontVariationSettings: "'FILL' 1" }}
                  >
                    location_on
                  </span>
                </div>
              </div>
              <p className="font-body-md text-on-surface font-semibold">
                Trilha da Cachoeira, Mata Atlântica
              </p>
              <p className="font-label-caps text-label-caps text-on-surface-variant">
                Lat: -23.5505, Long: -46.6333
              </p>
            </div>
          </section>
        </div>
      </main>

      {/* Botão fixo — desabilitado sem animal */}
      <button
        onClick={() => animal && setSheetOpen(true)}
        disabled={!animal}
        className={`fixed left-0 right-0 z-40 mx-container-margin
          w-[calc(100%-2*20px)] bottom-20
          flex items-center justify-center gap-md
          py-md rounded-xl font-headline-sm text-headline-sm shadow-sm
          active:scale-95 transition-transform
          ${animal
            ? 'bg-primary text-on-primary cursor-pointer'
            : 'bg-outline-variant text-on-surface-variant cursor-not-allowed'
          }`}
      >
        <span className="material-symbols-outlined">share</span>
        COMPARTILHAR RELATÓRIO
      </button>

      <BottomSheet open={sheetOpen} onClose={() => setSheetOpen(false)} />
      <BottomNav />
    </>
  )
}
