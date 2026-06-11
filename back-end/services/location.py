from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim(user_agent="soromais_backend")

def obter_endereco_por_coordenadas(lat: float, long: float) -> str:
    try:
        # Executa a geocodificação reversa
        location = geolocator.reverse(f"{lat}, {long}", timeout=5)
        if location:
            return location.address
        return "Endereço não encontrado"
    except GeocoderTimedOut:
        return "Erro de timeout ao buscar endereço"
    except Exception:
        return "Não foi possível determinar o ponto de referência"