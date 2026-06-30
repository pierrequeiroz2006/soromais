from pydantic import BaseModel
from typing import Literal, Optional

class AnaliseAnimal(BaseModel):
    especie: str
    lugar: str
    efeitos: str
    tempo_de_acao: str
    gravidade: Literal["Baixa", "Moderada", "Alta", "Extrema"]

class RespostaIdentificacao(BaseModel):
    status: str
    arquivo: str
    analise_ia: AnaliseAnimal
    foto_url: Optional[str] = None
