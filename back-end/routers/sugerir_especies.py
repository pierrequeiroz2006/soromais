import json
import asyncio
import logging

from fastapi import APIRouter, Form, HTTPException, Request
from typing import Optional
from dependencies import gemini_client
from schemas.sugestao import EspecieSugerida, RespostaSugestao
from services.wikimedia import buscar_imagem_especie
from security import sanitize_text
from limiter import limiter

logger = logging.getLogger("soromais")

router = APIRouter(prefix="/sugerir-especies", tags=["sugestoes"])

_SCHEMA_EXEMPLO = [
    {"nome_popular": "Nome popular da espécie", "nome_cientifico": "Nome científico da espécie"}
]


def _build_prompt(descricao: str, localizacao: str) -> str:
    contexto_geo = f"\nLocalização do incidente: {localizacao}" if localizacao else ""
    return f"""Você é um especialista em animais peçonhentos do Brasil.
Com base na descrição abaixo, retorne SOMENTE um array JSON com exatamente 4 espécies mais prováveis.
Sem texto adicional, sem markdown, sem explicações.{contexto_geo}

Descrição do animal: {descricao}

Regras:
- Considere apenas animais peçonhentos nativos do Brasil
- Use a localização (se fornecida) para priorizar espécies da região
- Ordene da mais para a menos provável
- Retorne exatamente 4 itens

Formato esperado:
{json.dumps(_SCHEMA_EXEMPLO * 4, ensure_ascii=False, indent=2)}
"""


@router.post("", response_model=RespostaSugestao)
@limiter.limit("15/minute")
async def sugerir_especies(
    request: Request,
    descricao: str = Form(...),
    ponto_ref: Optional[str] = Form(None),
    lat: Optional[float] = Form(None),
    lng: Optional[float] = Form(None),
):
    descricao = sanitize_text(descricao)
    localizacao = sanitize_text(ponto_ref) or (
        f"lat {lat}, lng {lng} (Brasil)" if lat and lng else ""
    )
    prompt = _build_prompt(descricao, localizacao)

    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"IA indisponível no momento: {str(e)}")

    raw = response.text.strip()
    logger.debug("Gemini (sugestões) response received (chars=%d)", len(raw))

    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

    try:
        especies = json.loads(raw)[:4]
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=422, detail=f"IA retornou resposta mal formatada: {str(e)}")

    imagens = await asyncio.gather(*[
        buscar_imagem_especie(e.get("nome_cientifico", "")) for e in especies
    ])

    sugestoes = [
        EspecieSugerida(
            nome_popular=e.get("nome_popular", ""),
            nome_cientifico=e.get("nome_cientifico", ""),
            imagem_url=img,
        )
        for e, img in zip(especies, imagens)
    ]

    return RespostaSugestao(sugestoes=sugestoes)
