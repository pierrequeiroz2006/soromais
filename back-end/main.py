from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from dotenv import load_dotenv
import os

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
def salvar_relatorio(dados: dict):
    response = supabase.table("paciente").insert(dados).execute()
    return response.data