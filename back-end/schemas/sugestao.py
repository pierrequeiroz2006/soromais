from pydantic import BaseModel
from typing import Optional


class EspecieSugerida(BaseModel):
    nome_popular: str
    nome_cientifico: str
    imagem_url: Optional[str] = None


class RespostaSugestao(BaseModel):
    sugestoes: list[EspecieSugerida]