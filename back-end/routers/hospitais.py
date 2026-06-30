from fastapi import APIRouter
from schemas.hospital import Hospital
from dependencies import supabase

router = APIRouter(prefix="/hospitais", tags=["hospitais"])


@router.get("", response_model=list[dict])
def get_hospitais():
    response = supabase.table("hospital").select("*").execute()
    return response.data


@router.get("/proximos", response_model=list[Hospital])
def hospitais_proximos(lat: float, lng: float):
    response = supabase.rpc("buscar_hospitais_proximos", {"user_lat": lat, "user_lng": lng}).execute()
    return response.data