import json
import os
import uuid
import logging

import filetype
from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from typing import Optional
from google.genai import types
from schemas.animal import RespostaIdentificacao
from dependencies import gemini_client, supabase
from security import sanitize_text, sanitize_o_que_fazer
from limiter import limiter

logger = logging.getLogger("soromais")

router = APIRouter(prefix="/identificar-animal", tags=["identificacao"])

_MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_BYTES", str(10 * 1024 * 1024)))
_ALLOWED_IMAGE_EXT = {"jpg", "jpeg", "png", "webp", "gif"}

_ANIMAL_SCHEMA = {
    "especie": "Nome popular (ex: Escorpião-amarelo)",
    "lugar": "Regiões do país e habitats comuns onde é encontrado",
    "efeitos": "Principais sintomas e efeitos do veneno no corpo humano",
    "tempo_de_acao": "Tempo estimado para agravamento ou risco de morte sem socorro",
    "gravidade": "Nível de urgência: exatamente um de ['Baixa', 'Moderada', 'Alta', 'Extrema']",
    "o_que_fazer": "Primeiros socorros específicos para esse animal, do momento da picada/ataque até a chegada ao hospital",
}

_GRAVIDADES_VALIDAS = {"Baixa", "Moderada", "Alta", "Extrema"}


def _build_prompt(localizacao: str) -> str:
    contexto_geo = f"\nLocalização do incidente: {localizacao}" if localizacao else ""
    return f"""Você é um especialista em animais peçonhentos do Brasil.
Analise a imagem e retorne SOMENTE um objeto JSON válido, sem texto adicional, sem markdown, sem explicações.{contexto_geo}

Regras para os valores:
- Sem emojis em nenhum campo
- Textos curtos e diretos, máximo 2 linhas por campo
- O campo "efeitos" deve ser uma lista de 3 a 4 tópicos separados por '\\n', cada um começando com '- '
- O campo "lugar" deve citar apenas regiões/biomas, sem detalhes extensos
- O campo "tempo_de_acao" deve ser uma frase curta (ex: "Sintomas em 30min, risco de morte em 6-24h sem tratamento")
- O campo "o_que_fazer" deve ser uma lista de 4 a 5 tópicos separados por '\\n', cada um começando com '- ', com condutas de primeiros socorros ESPECÍFICAS para esse animal (ex: se for cobra peçonhenta, orientar a manter o membro imobilizado e abaixo do nível do coração; se for aranha ou escorpião, orientar compressa fria; NUNCA sugerir torniquete, sucção, cortes ou remédios caseiros). A foto do animal já foi enviada e a espécie já foi identificada — NUNCA inclua orientações como "tire uma foto do animal" ou "fotografe o animal para identificação"
- Use a localização do incidente (se fornecida) para priorizar espécies nativas dessa região

O JSON deve ter exatamente estas chaves:
{json.dumps(_ANIMAL_SCHEMA, ensure_ascii=False, indent=2)}
"""


@router.post("", response_model=RespostaIdentificacao)
@limiter.limit("10/minute")
async def identificar_animal(
    request: Request,
    file: UploadFile = File(...),
    lat: Optional[float] = Form(None),
    lng: Optional[float] = Form(None),
    ponto_ref: Optional[str] = Form(None),
):
    imagem_bytes = await file.read()

    if len(imagem_bytes) > _MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Arquivo muito grande")
    kind = filetype.guess(imagem_bytes)
    if kind is None or kind.extension.lower() not in _ALLOWED_IMAGE_EXT:
        raise HTTPException(status_code=415, detail="Tipo de arquivo não suportado")
    extensao = "jpg" if kind.extension.lower() in ("jpg", "jpeg") else kind.extension.lower()
    mime_type = "image/jpeg" if extensao == "jpg" else f"image/{extensao}"

    nome_arquivo = f"{uuid.uuid4()}.{extensao}"
    supabase.storage.from_("fotos-animais").upload(
        nome_arquivo, imagem_bytes, {"content-type": mime_type}
    )
    foto_url = supabase.storage.from_("fotos-animais").get_public_url(nome_arquivo)

    localizacao = sanitize_text(ponto_ref) or (
        f"lat {lat}, lng {lng} (Brasil)" if lat and lng else ""
    )
    prompt = _build_prompt(localizacao)

    conteudo = [
        types.Part.from_bytes(data=imagem_bytes, mime_type=mime_type),
        prompt,
    ]

    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=conteudo,
        )

        raw = response.text.strip()
        logger.debug("Gemini response received (chars=%d)", len(raw))

        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

        analise = json.loads(raw)

        if analise.get("gravidade") not in _GRAVIDADES_VALIDAS:
            analise["gravidade"] = "Moderada"

        analise["o_que_fazer"] = sanitize_o_que_fazer(analise.get("o_que_fazer"))

        return RespostaIdentificacao(
            status="sucesso",
            arquivo=file.filename,
            analise_ia=analise,
            foto_url=foto_url,
        )

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=422, detail=f"IA retornou resposta mal formatada: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Não foi possível processar a imagem: {str(e)}")


@router.post("/por-nome", response_model=RespostaIdentificacao)
@limiter.limit("10/minute")
async def identificar_por_nome(
    request: Request,
    nome_animal: str = Form(...),
):
    nome_animal = sanitize_text(nome_animal)
    prompt = f"""Você é um especialista em animais peçonhentos do Brasil.
A espécie é "{nome_animal}". Retorne SOMENTE um objeto JSON válido, sem texto adicional, sem markdown, sem explicações.

Regras para os valores:
- Sem emojis em nenhum campo
- Textos curtos e diretos, máximo 2 linhas por campo
- O campo "efeitos" deve ser uma lista de 3 a 4 tópicos separados por '\\n', cada um começando com '- '
- O campo "lugar" deve citar apenas regiões/biomas, sem detalhes extensos
- O campo "tempo_de_acao" deve ser uma frase curta (ex: "Sintomas em 30min, risco de morte em 6-24h sem tratamento")
- O campo "o_que_fazer" deve ser uma lista de 4 a 5 tópicos separados por '\\n', cada um começando com '- ', com condutas de primeiros socorros ESPECÍFICAS para esse animal (ex: se for cobra peçonhenta, orientar a manter o membro imobilizado e abaixo do nível do coração; se for aranha ou escorpião, orientar compressa fria; NUNCA sugerir torniquete, sucção, cortes ou remédios caseiros). A foto do animal já foi enviada e a espécie já foi identificada — NUNCA inclua orientações como "tire uma foto do animal" ou "fotografe o animal para identificação"

O JSON deve ter exatamente estas chaves:
{json.dumps(_ANIMAL_SCHEMA, ensure_ascii=False, indent=2)}
"""

    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        raw = response.text.strip()
        logger.debug("Gemini (por-nome) response received (chars=%d)", len(raw))

        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

        analise = json.loads(raw)

        if analise.get("gravidade") not in _GRAVIDADES_VALIDAS:
            analise["gravidade"] = "Moderada"

        analise["o_que_fazer"] = sanitize_o_que_fazer(analise.get("o_que_fazer"))

        return RespostaIdentificacao(
            status="sucesso",
            arquivo=nome_animal,
            analise_ia=analise,
        )

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=422, detail=f"IA retornou resposta mal formatada: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Não foi possível processar: {str(e)}")
