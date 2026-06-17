import requests
from pathlib import Path

BASE = Path(__file__).parent.parent

ESTADOS = [
    "paraiba"
]

URL_BASE = "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/animais-peconhentos/hospitais-de-referencia/{estado_selecionado}/@@download/file"

path_pdfs = BASE / "pdfs"
path_pdfs.mkdir(exist_ok=True)

for estado in ESTADOS:

    url = URL_BASE.format(estado_selecionado=estado)
    response = requests.get(url, timeout=30)

    if response.status_code == 200:

        with open(path_pdfs / f"{estado}.pdf", "wb") as f:
            f.write(response.content)
        print(f"✓ {estado.upper()} baixado")

    else:
        print(f"✗ {estado.upper()} — status {response.status_code}")
    
    
