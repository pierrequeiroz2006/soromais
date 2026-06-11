import os
from fastapi import APIRouter
from twilio.rest import Client
from ..schemas.relatorio import DadosWhatsApp
from ..dependencies import supabase

router = APIRouter(prefix="/enviar-whatsapp", tags=["notificacao"])


@router.post("")
async def enviar_whatsapp(dados: DadosWhatsApp):
    hospital = supabase.table("hospital").select("*").eq("id", dados.hospital_id).execute()

    if not hospital.data:
        return {"erro": "Hospital não encontrado"}

    telefone = hospital.data[0].get("telefone")
    if not telefone:
        return {"erro": "Hospital sem telefone cadastrado"}

    twilio = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

    mensagem = f"""
*RELATÓRIO DE ACIDENTE - SOROMAIS*

*Paciente:* {dados.nome or 'Não informado'}
*Idade:* {dados.idade or 'Não informado'} anos
*Peso:* {dados.peso or 'Não informado'} kg
*Estado:* {dados.estado or 'Não informado'}

*Animal:* {dados.animal or 'Não identificado'}
*Local da picada:* {dados.localPicada or 'Não informado'}
*Tempo decorrido:* {dados.tempo or 'Não informado'} min
*Localização:* {dados.localizacao or 'Não informada'}
    """.strip()

    message = twilio.messages.create(
        from_=f"whatsapp:{os.getenv('TWILIO_WHATSAPP_NUMBER')}", # <--- Garanta o prefixo aqui
        body=mensagem,
        to=f"whatsapp:{telefone}",
    )

    return {"sucesso": True, "sid": message.sid}