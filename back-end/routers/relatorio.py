import logging

from fastapi import APIRouter, Request
from schemas.relatorio import DadosRelatorio
from dependencies import supabase
from services.location import obter_endereco_por_coordenadas
from security import sanitize_text
from limiter import limiter

logger = logging.getLogger("soromais")

router = APIRouter(prefix="/relatorio", tags=["relatorio"])


@router.post("")
@limiter.limit("20/minute")
async def salvar_relatorio(request: Request, dados: DadosRelatorio):
    localizacao_id = None
    ponto_referencia = sanitize_text(dados.ponto_ref)
    if dados.lat and dados.lng:
        if not ponto_referencia:
            ponto_referencia = obter_endereco_por_coordenadas(dados.lat, dados.lng)

        local = {
            "lat": dados.lat,
            "long": dados.lng,
            "ponto_ref": ponto_referencia,
            "nome": sanitize_text(dados.nome_local),
            "urbano_rural": dados.urbano_rural,
        }
        local_response = supabase.table("local").insert(local).execute()
        localizacao_id = local_response.data[0]["id"]

    paciente = {
        "nome_do_paciente": dados.nome,
        "idade": dados.idade,
        "peso": dados.peso,
        "tempo_decorrido": dados.tempo,
        "local_da_picada": dados.localPicada,
        "estado_do_paciente": dados.estado,
        "localizacao": localizacao_id,
    }
    paciente_response = supabase.table("paciente").insert(paciente).execute()

    return {"sucesso": True, "paciente": paciente_response.data[0]}

@router.get("/buscar-endereco")
@limiter.limit("30/minute")
async def buscar_endereco(request: Request, lat: float, lng: float):
    endereco = obter_endereco_por_coordenadas(lat, lng)
    return {"endereco": endereco}
