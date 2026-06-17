import os
import httpx
from fastapi import APIRouter
from ..schemas.hospital import Hospital
from ..dependencies import supabase

router = APIRouter(prefix="/hospitais", tags=["hospitais"])


@router.get("", response_model=list[dict])
def get_hospitais():
    response = supabase.table("hospital").select("*").execute()
    return response.data


@router.get("/proximos", response_model=list[Hospital])
async def hospitais_proximos(lat: float, lng: float):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": 10000,
        "keyword": "hospital soro antiofidico",
        "language": "pt-BR",
        "key": os.getenv("GOOGLE_MAPS_KEY"),
    }

    async with httpx.AsyncClient() as http:
        response = await http.get(url, params=params)
        data = response.json()

    return [
        HospitalProximo(
            nome=place.get("name"),
            endereco=place.get("vicinity"),
            lat=place["geometry"]["location"]["lat"],
            lng=place["geometry"]["location"]["lng"],
            aberto=place.get("opening_hours", {}).get("open_now"),
        )
        for place in data.get("results", [])
    ]