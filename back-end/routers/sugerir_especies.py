import json
import asyncio
from fastapi import APIRouter, Form
from typing import Optional
from ..dependencies import gemini_client
from ..schemas.sugestao import EspecieSugerida, RespostaSugestao
from ..services.wikimedia import buscar_imagem_especie

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
async def sugerir_especies(
    descricao: str = Form(...),
    ponto_ref: Optional[str] = Form(None),
    lat: Optional[float] = Form(None),
    lng: Optional[float] = Form(None),
):
    localizacao = ponto_ref or (f"lat {lat}, lng {lng} (Brasil)" if lat and lng else "")
    prompt = _build_prompt(descricao, localizacao)

    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    raw = response.text.strip()
    print("\n=== GEMINI SUGESTÕES ===\n", raw, "\n=======================\n")

    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

    especies = json.loads(raw)[:4]

    imagens = await asyncio.gather(*[
        buscar_imagem_especie(e["nome_cientifico"]) for e in especies
    ])

    sugestoes = [
        EspecieSugerida(
            nome_popular=e["nome_popular"],
            nome_cientifico=e["nome_cientifico"],
            imagem_url=img,
        )
        for e, img in zip(especies, imagens)
    ]

    return RespostaSugestao(sugestoes=sugestoes)