import os
import logging

from dotenv import load_dotenv

load_dotenv()

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from routers import hospitais, relatorio, whatsapp, identificacao, sugerir_especies
from security import require_auth
from limiter import limiter

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("soromais")

ALLOWED_ORIGINS = [
    o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()
]

app = FastAPI(title="SoroMais API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.getenv("API_KEY") and not os.getenv("JWT_SECRET"):
    logger.warning(
        "API AUTH DISABLED: set API_KEY (or JWT_SECRET) before deploying to production."
    )
app.include_router(hospitais.router, dependencies=[Depends(require_auth)])
app.include_router(relatorio.router, dependencies=[Depends(require_auth)])
app.include_router(whatsapp.router, dependencies=[Depends(require_auth)])
app.include_router(identificacao.router, dependencies=[Depends(require_auth)])
app.include_router(sugerir_especies.router, dependencies=[Depends(require_auth)])


@app.get("/")
def home():
    return {"mensagem": "API do SoroMais funcionando!"}
