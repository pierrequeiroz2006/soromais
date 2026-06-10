from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from dotenv import load_dotenv
import os
import httpx
from twilio.rest import Client
from google import genai
import json
from google.genai import types

# Carrega as variáveis do .env
load_dotenv()

# Conecta com o Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Cria o app FastAPI
app = FastAPI()

# Inicializa o cliente do Gemini (ele busca automaticamente o GEMINI_API_KEY do seu .env)
client = genai.Client()

# Permite o front-end conversar com o back-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rota de teste
@app.get("/")
def home():
    return {"mensagem": "API do SoroMais funcionando!"}

# Buscar todos os hospitais
@app.get("/hospitais")
def get_hospitais():
    response = supabase.table("hospital").select("*").execute()
    return response.data

# Salvar relatório da vítima
@app.post("/relatorio")
async def salvar_relatorio(dados: dict):
    # 1. Salva a localização primeiro
    localizacao_id = None
    if dados.get("lat") and dados.get("lng"):
        local = {
            "lat": dados["lat"],
            "long": dados["lng"],
            "ponto_ref": dados.get("ponto_ref"),
            "nome": dados.get("nome_local"),
            "urbano_rural": dados.get("urbano_rural")
        }
        local_response = supabase.table("local").insert(local).execute()
        localizacao_id = local_response.data[0]["id"]

    # 2. Salva o paciente com o id da localização
    paciente = {
        "nome_do_paciente": dados.get("nome"),
        "idade": dados.get("idade"),
        "peso": dados.get("peso"),
        "tempo_decorrido": dados.get("tempo"),
        "local_da_picada": dados.get("localPicada"),
        "estado_do_paciente": dados.get("estado"),
        "localizacao": localizacao_id
    }
    paciente_response = supabase.table("paciente").insert(paciente).execute()

    return {"sucesso": True, "paciente": paciente_response.data[0]}

# Buscar hospitais próximos pelo Google Maps
@app.get("/hospitais-proximos")
async def hospitais_proximos(lat: float, lng: float):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": 10000,
        "keyword": "hospital soro antiofidico",
        "language": "pt-BR",
        "key": os.getenv("GOOGLE_MAPS_KEY")
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

    hospitais = []
    for place in data.get("results", []):
        hospitais.append({
            "nome": place.get("name"),
            "endereco": place.get("vicinity"),
            "lat": place["geometry"]["location"]["lat"],
            "lng": place["geometry"]["location"]["lng"],
            "aberto": place.get("opening_hours", {}).get("open_now")
        })

    return hospitais

from twilio.rest import Client

@app.post("/enviar-whatsapp")
async def enviar_whatsapp(dados: dict):
    # Busca o telefone do hospital no banco
    hospital = supabase.table("hospital").select("*").eq("id", dados.get("hospital_id")).execute()
    
    if not hospital.data:
        return {"erro": "Hospital não encontrado"}
    
    telefone = hospital.data[0].get("telefone")
    if not telefone:
        return {"erro": "Hospital sem telefone cadastrado"}

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    mensagem = f"""
*RELATÓRIO DE ACIDENTE - SOROMAIS*

*Paciente:* {dados.get('nome', 'Não informado')}
*Idade:* {dados.get('idade', 'Não informado')} anos
*Peso:* {dados.get('peso', 'Não informado')} kg
*Estado:* {dados.get('estado', 'Não informado')}

*Animal:* {dados.get('animal', 'Não identificado')}
*Local da picada:* {dados.get('localPicada', 'Não informado')}
*Tempo decorrido:* {dados.get('tempo', 'Não informado')} min
*Localização:* {dados.get('localizacao', 'Não informada')}
    """

    message = client.messages.create(
        from_=os.getenv("TWILIO_WHATSAPP_NUMBER"),
        body=mensagem,
        to=f"whatsapp:{telefone}"
    )

    return {"sucesso": True, "sid": message.sid}

# =======================================================
# NOVA ROTA: IDENTIFICAÇÃO DO ANIMAL COM GEMINI
# =======================================================

# Schema inline — sem problema manter aqui dado o escopo do projeto
ANIMAL_SCHEMA = {
    "especie": "Nome popular e científico (ex: Escorpião-amarelo / Tityus serrulatus)",
    "lugar": "Regiões do país e habitats comuns onde é encontrado",
    "efeitos": "Principais sintomas e efeitos do veneno no corpo humano",
    "tempo_de_acao": "Tempo estimado para agravamento ou risco de morte sem socorro",
    "gravidade": "Nível de urgência: exatamente um de ['Baixa', 'Moderada', 'Alta', 'Extrema']"
}

PROMPT_IDENTIFICACAO = f"""Você é um especialista em animais peçonhentos do Brasil.
Analise a imagem e retorne SOMENTE um objeto JSON válido, sem texto adicional, sem markdown, sem explicações.

Regras para os valores:
- Sem emojis em nenhum campo
- Textos curtos e diretos, máximo 2 linhas por campo
- O campo "efeitos" deve ser uma lista de 3 a 4 tópicos separados por '\\n', cada um começando com '- '
- O campo "lugar" deve citar apenas regiões/biomas, sem detalhes extensos
- O campo "tempo_de_acao" deve ser uma frase curta (ex: "Sintomas em 30min, risco de morte em 6-24h sem tratamento")

O JSON deve ter exatamente estas chaves:
{json.dumps(ANIMAL_SCHEMA, ensure_ascii=False, indent=2)}
"""

@app.post("/identificar-animal")
async def identificar_animal(file: UploadFile = File(...)):
    imagem_bytes = await file.read()

    # Detecta o mime type a partir do content_type do upload
    mime_type = file.content_type or "image/jpeg"

    conteudo_envio = [
        types.Part.from_bytes(data=imagem_bytes, mime_type=mime_type),
        PROMPT_IDENTIFICACAO,
    ]

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=conteudo_envio,
        )

        raw_text = response.text.strip()
        print("\n=== RESPOSTA DO GEMINI ===\n", raw_text, "\n==========================\n")

        # Remove cercas de markdown caso o modelo desobedeça o prompt
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[-1]
            raw_text = raw_text.rsplit("```", 1)[0].strip()

        analise = json.loads(raw_text)

        # Garante que gravidade está dentro dos valores válidos
        valores_validos = {"Baixa", "Moderada", "Alta", "Extrema"}
        if analise.get("gravidade") not in valores_validos:
            analise["gravidade"] = "Moderada"  # fallback seguro

        return {
            "status": "sucesso",
            "arquivo": file.filename,
            "analise_ia": analise,  # agora é um dict, não string
        }

    except json.JSONDecodeError as e:
        return {"erro": f"IA retornou resposta mal formatada: {str(e)}", "raw": raw_text}
    except Exception as e:
        return {"erro": f"Não foi possível processar a imagem: {str(e)}"}