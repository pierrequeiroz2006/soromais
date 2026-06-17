from pydantic import BaseModel
from typing import Optional


class Hospital(BaseModel):
    cnes: str
    nome: str
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None