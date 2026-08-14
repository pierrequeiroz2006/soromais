import logging

from fastapi import APIRouter, Request
from schemas.hospital import Hospital
from dependencies import supabase
from limiter import limiter

logger = logging.getLogger("soromais")

router = APIRouter(prefix="/hospitais", tags=["hospitais"])


@router.get("", response_model=list[dict])
@limiter.limit("60/minute")
def get_hospitais(request: Request):
    response = supabase.table("hospital").select("*").execute()
    return response.data


@router.get("/proximos", response_model=list[Hospital])
@limiter.limit("60/minute")
def hospitais_proximos(request: Request, lat: float, lng: float):
    response = supabase.rpc("buscar_hospitais_proximos", {"user_lat": lat, "user_lng": lng}).execute()
    return response.data