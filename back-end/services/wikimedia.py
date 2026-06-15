import httpx
from urllib.parse import quote

_HEADERS = {"User-Agent": "SoroMais/1.0 (aplicativo educacional de identificacao de animais peconhentos)"}


async def buscar_imagem_especie(nome_cientifico: str) -> str | None:
    async with httpx.AsyncClient(timeout=8, headers=_HEADERS) as client:
        # iNaturalist — fonte principal, tem fotos de quase todas as espécies brasileiras
        try:
            url = f"https://api.inaturalist.org/v1/taxa?q={quote(nome_cientifico)}&per_page=1&rank=species"
            resp = await client.get(url)
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                if results:
                    photo = results[0].get("default_photo") or {}
                    imagem = photo.get("medium_url") or photo.get("url")
                    if imagem:
                        return imagem
        except Exception:
            pass

        # Fallback: Wikipedia
        nome_url = quote(nome_cientifico.replace(" ", "_"))
        for lang in ("en", "pt"):
            try:
                url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{nome_url}"
                resp = await client.get(url, follow_redirects=True)
                if resp.status_code == 200:
                    thumbnail = resp.json().get("thumbnail", {}).get("source")
                    if thumbnail:
                        return thumbnail
            except Exception:
                continue

    return None