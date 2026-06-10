import json
from fastapi import APIRouter, File, UploadFile
from google.genai import types
from ..schemas.animal import RespostaIdentificacao
from ..dependencies import gemini_client

router = APIRouter(prefix="/identificar-animal", tags=["identificacao"])

_ANIMAL_SCHEMA = {
    "especie": "Nome popular e científico (ex: Escorpião-amarelo / Tityus serrulatus)",
    "lugar": "Regiões do país e habitats comuns onde é encontrado",
    "efeitos": "Principais sintomas e efeitos do veneno no corpo humano",
    "tempo_de_acao": "Tempo estimado para agravamento ou risco de morte sem socorro",
    "gravidade": "Nível de urgência: exatamente um de ['Baixa', 'Moderada', 'Alta', 'Extrema']",
}

_PROMPT = f"""Você é um especialista em animais peçonhentos do Brasil.
Analise a imagem e retorne SOMENTE um objeto JSON válido, sem texto adicional, sem markdown, sem explicações.

Regras para os valores:
- Sem emojis em nenhum campo
- Textos curtos e diretos, máximo 2 linhas por campo
- O campo "efeitos" deve ser uma lista de 3 a 4 tópicos separados por '\\n', cada um começando com '- '
- O campo "lugar" deve citar apenas regiões/biomas, sem detalhes extensos
- O campo "tempo_de_acao" deve ser uma frase curta (ex: "Sintomas em 30min, risco de morte em 6-24h sem tratamento")

O JSON deve ter exatamente estas chaves:
{json.dumps(_ANIMAL_SCHEMA, ensure_ascii=False, indent=2)}
"""

_GRAVIDADES_VALIDAS = {"Baixa", "Moderada", "Alta", "Extrema"}


@router.post("", response_model=RespostaIdentificacao)
async def identificar_animal(file: UploadFile = File(...)):
    imagem_bytes = await file.read()
    mime_type = file.content_type or "image/jpeg"

    conteudo = [
        types.Part.from_bytes(data=imagem_bytes, mime_type=mime_type),
        _PROMPT,
    ]

    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=conteudo,
        )

        raw = response.text.strip()
        print("\n=== GEMINI ===\n", raw, "\n==============\n")

        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

        analise = json.loads(raw)

        if analise.get("gravidade") not in _GRAVIDADES_VALIDAS:
            analise["gravidade"] = "Moderada"

        return RespostaIdentificacao(
            status="sucesso",
            arquivo=file.filename,
            analise_ia=analise,
        )

    except json.JSONDecodeError as e:
        return {"erro": f"IA retornou resposta mal formatada: {str(e)}", "raw": raw}
    except Exception as e:
        return {"erro": f"Não foi possível processar a imagem: {str(e)}"}