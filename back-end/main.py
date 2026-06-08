from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from dotenv import load_dotenv
import os
import httpx

# Carrega as variáveis do .env
load_dotenv()

# Conecta com o Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Cria o app FastAPI
app = FastAPI()

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