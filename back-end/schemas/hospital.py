from pydantic import BaseModel
from typing import Optional


class HospitalProximo(BaseModel):
    nome: str
    endereco: str
    lat: float
    lng: float
    aberto: Optional[bool] = None