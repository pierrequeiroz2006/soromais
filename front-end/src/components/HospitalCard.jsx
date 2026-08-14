import { useState } from 'react'
import { apiFetch } from '../api'

export default function HospitalCard({ hospital, featured = false, variant = 'full', dadosRelatorio, onEnviado }) {
  const { id, nome, endereco, distancia, tempo, telefone, lat, lng } = hospital
  const [enviando, setEnviando] = useState(false)
  const [erro, setErro] = useState(null)
  const [enviado, setEnviado] = useState(false)

  const handleEnviar = async () => {
    if (!id) {
      setErro('Hospital sem ID')
      return
    }
    setEnviando(true)
    setErro(null)
    try {
      const resposta = await apiFetch(`/enviar-whatsapp`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ hospital_id: id, ...dadosRelatorio }),
      })
      const dados = await resposta.json()
      if (!resposta.ok || dados.erro) {
        setErro(dados.erro || dados.detail || 'Erro ao enviar')
      } else {
        setEnviado(true)
        if (onEnviado) onEnviado()
      }
    } catch (e) {
      setErro(e.message)
    } finally {
      setEnviando(false)
    }
  }

  if (variant === 'sheet') {
    return (
      <div className={`p-md rounded-xl flex justify-between items-center
        ${featured
          ? 'border-2 border-primary bg-primary-container/10'
          : 'border border-outline-variant'
        }`}
      >
        <div className="flex flex-col">
          {featured && (
            <span className="font-label-caps text-[10px] text-primary font-bold mb-1 uppercase">
              Referência
            </span>
          )}
          <span className="font-body-lg font-bold text-on-surface">{nome}</span>
          {distancia && (
            <span className="font-label-caps text-on-surface-variant text-[11px]">
              {distancia}
            </span>
          )}
          {erro && <span className="text-error text-[11px] mt-1">{erro}</span>}
        </div>
        <button
          onClick={handleEnviar}
          disabled={enviando || enviado}
          className={`px-lg py-sm rounded-full font-label-caps text-label-caps active:scale-95 transition-all
          ${featured
            ? 'bg-primary text-on-primary shadow-sm hover:brightness-110'
            : 'border border-primary text-primary hover:bg-primary/5'
          } ${(enviando || enviado) ? 'opacity-60 cursor-not-allowed' : ''}`}
        >
          {enviado ? 'ENVIADO' : enviando ? 'ENVIANDO...' : 'ENVIAR'}
        </button>
      </div>
    )
  }
  return (
    <div className={`bg-white rounded-xl p-md shadow-sm
      ${featured ? 'border-2 border-primary' : 'border border-outline-variant'}`}
    >
      <div className="flex justify-between items-start mb-2">
        <div className="flex-1">
          {featured && (
            <span className="inline-block bg-primary text-white text-[11px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider mb-2">
              Mais Rápido
            </span>
          )}
          <h3 className="text-xl font-bold text-on-surface leading-tight">{nome}</h3>
          <p className="text-on-surface-variant text-sm font-medium mt-1">{endereco}</p>
        </div>
        <div className="text-right shrink-0 ml-4">
          <div className={`text-xl font-bold ${featured ? 'text-primary' : 'text-on-surface'}`}>
            {distancia}
          </div>
          <div className="text-sm font-semibold text-on-surface-variant">{tempo}</div>
        </div>
      </div>
      <div className="flex items-center gap-1.5 mb-md bg-secondary-container/30 w-fit px-3 py-1 rounded-lg">
        <span className="material-symbols-outlined text-primary text-lg" style={{ fontVariationSettings: "'FILL' 1" }}>
          verified
        </span>
        <span className="text-sm font-bold text-primary">Soro disponível</span>
      </div>
      <div className="flex gap-3">
        <a href={`https://maps.google.com/?q=${lat},${lng}`} target="_blank" rel="noreferrer" className="flex-1 h-[52px] bg-primary text-white rounded-xl font-bold flex justify-center items-center gap-2 active:scale-95 transition-transform">
          <span className="material-symbols-outlined">directions</span>
          Rota
        </a>
        <a href={`tel:${telefone}`} className="flex-1 h-[52px] border-2 border-primary text-primary rounded-xl font-bold flex justify-center items-center gap-2 active:scale-95 transition-transform">
          <span className="material-symbols-outlined">call</span>
          Ligar
        </a>
      </div>
    </div>
  )
}
