from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim(user_agent="soromais_backend")

def obter_endereco_por_coordenadas(lat: float, long: float) -> str | None:
    try:
        # Executa a geocodificação reversa
        location = geolocator.reverse(f"{lat}, {long}", timeout=8)
        if location:
            return location.address
        return None
    except GeocoderTimedOut:
        return None
    except Exception:
        return None