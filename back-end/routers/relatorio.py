from fastapi import APIRouter
from ..schemas.relatorio import DadosRelatorio
from ..dependencies import supabase

router = APIRouter(prefix="/relatorio", tags=["relatorio"])


@router.post("")
async def salvar_relatorio(dados: DadosRelatorio):
    localizacao_id = None

    if dados.lat and dados.lng:
        local = {
            "lat": dados.lat,
            "long": dados.lng,
            "ponto_ref": dados.ponto_ref,
            "nome": dados.nome_local,
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