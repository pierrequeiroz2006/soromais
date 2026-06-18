import json
import os
from pathlib import Path
from supabase import create_client
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY"),
)

path_json = Path(__file__).parent / "data/output/hospitais.json"

with open(path_json, encoding="utf-8") as f:
    hospitais = json.load(f)

registros = []
for h in hospitais:
    endereco = " ".join(filter(None, [
        h.get("NO_LOGRADOURO", "").strip(),
        str(h.get("NU_ENDERECO", "")).strip(),
        h.get("NO_BAIRRO", "").strip(),
    ]))

    registros.append({
        "cnes": str(h.get("cnes") or "").strip() or None,
        "nome": (h.get("NO_FANTASIA") or "").strip().title() or None,
        "endereco": endereco.title() or None,
        "telefone": str(h.get("NU_TELEFONE") or "").strip() or None,
        "email": (h.get("NO_EMAIL") or "").strip() or None,
        "lat": h.get("NU_LATITUDE") or None,
        "lng": h.get("NU_LONGITUDE") or None,
    })

supabase.table("hospital").upsert(registros, on_conflict="cnes").execute()

print(f"✓ {len(registros)} hospitais inseridos/atualizados")
