from fastapi import APIRouter
from ..schemas.relatorio import DadosRelatorio
from ..dependencies import supabase
from ..services.location import obter_endereco_por_coordenadas 

router = APIRouter(prefix="/relatorio", tags=["relatorio"])


@router.post("")
async def salvar_relatorio(dados: DadosRelatorio):
    localizacao_id = None
    if dados.lat and dados.lng:
        ponto_referencia = dados.ponto_ref
        if not ponto_referencia:
            ponto_referencia = obter_endereco_por_coordenadas(dados.lat, dados.lng)
        # ---------------------------------------

        local = {
            "lat": dados.lat,
            "long": dados.lng,
            "ponto_ref": ponto_referencia, 
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

@router.get("/buscar-endereco")
async def buscar_endereco(lat: float, lng: float):
    # Chama a função tradutora que criamos
    endereco = obter_endereco_por_coordenadas(lat, lng)
    return {"endereco": endereco}