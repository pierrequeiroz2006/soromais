from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Hospital(BaseModel):
    id: UUID
    cnes: str
    nome: str
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
