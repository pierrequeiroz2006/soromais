from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import hospitais, relatorio, whatsapp, identificacao

app = FastAPI(title="SoroMais API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hospitais.router)
app.include_router(relatorio.router)
app.include_router(whatsapp.router)
app.include_router(identificacao.router)


@app.get("/")
def home():
    return {"mensagem": "API do SoroMais funcionando!"}