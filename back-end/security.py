import os
import re
import logging
import secrets

import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials

logger = logging.getLogger("soromais")

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "X-API-Key"
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
http_bearer = HTTPBearer(auto_error=False)


async def require_auth(
    api_key: str = Security(api_key_header),
    creds: HTTPAuthorizationCredentials = Security(http_bearer),
):
    if not API_KEY and not JWT_SECRET:
        return

    if API_KEY and api_key and secrets.compare_digest(api_key, API_KEY):
        return

    if JWT_SECRET and creds and creds.credentials:
        try:
            jwt.decode(creds.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return
        except jwt.PyJWTError as exc:
            logger.debug("Rejected JWT: %s", exc)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

_CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
MAX_USER_INPUT_LEN = int(os.getenv("MAX_USER_INPUT_LEN", "300"))


def sanitize_text(value: str | None, max_len: int = MAX_USER_INPUT_LEN) -> str:
    if not value:
        return ""
    value = _CONTROL_RE.sub(" ", value)
    value = " ".join(value.split())  # collapse all whitespace incl. newlines
    return value.strip()[:max_len]


_FORBIDDEN_FIRST_AID = [
    "torniquete",
    "sucção",
    "succao",
    "sugar",
    "chupar",
    "cortar",
    "corte",
    "cortes",
    "incis",
    "serrar",
    "remédio caseiro",
    "remedio caseiro",
    "pomada caseira",
    "chá",
    "cha",
    "cauteriz",
    "fogo",
    "bicarbonato",
    "álcool",
    "alcool",
    "limão",
    "limao",
    "vinagre",
    "café",
    "cafe",
    "garrafa",
]
_FORBIDDEN_RE = re.compile(
    r"\b(" + "|".join(re.escape(t) for t in _FORBIDDEN_FIRST_AID) + r")\b",
    re.IGNORECASE,
)

_SAFE_FALLBACK = (
    "- Lave o local com água e sabão, sem esfregar\n"
    "- Mantenha a vítima calma e imobilize o membro atingido, abaixo do nível do coração\n"
    "- Procure o hospital mais próximo levando o paciente e o horário do acidente"
)


def sanitize_o_que_fazer(text: str | None) -> str:
    if not text:
        return _SAFE_FALLBACK
    safe_lines = []
    for raw in text.split("\n"):
        line = raw.strip()
        if not line:
            continue
        if _FORBIDDEN_RE.search(line):
            logger.warning("Removed unsafe first-aid guidance: %s", line[:80])
            continue
        safe_lines.append(line)
    return "\n".join(safe_lines) if safe_lines else _SAFE_FALLBACK
