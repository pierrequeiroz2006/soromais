# Etapa 1a do pipeline (back-end/scripts/pipeline.py): baixa o(s) PDF(s) de "hospitais de
# referência para atendimento de acidentes por animais peçonhentos" do Ministério da Saúde,
# um por estado em ESTADOS, e salva em back-end/scripts/pdfs/{estado}.pdf.
#
# ATENÇÃO: a página do gov.br passou a exigir autenticação/login para acessar esse PDF. O
# request abaixo então recebe HTTP 200 com uma página HTML de erro ("é necessário autenticar"),
# não o PDF em si — e como só checamos o status_code, esse HTML acaba sendo salvo como .pdf,
# quebrando o parse_pdfs.py mais adiante com "No /Root object!". Nesse caso, baixe o PDF
# manualmente (logado no navegador) e coloque em pdfs/{estado}.pdf; o pipeline.py detecta o
# arquivo existente e pergunta se quer reaproveitá-lo em vez de rodar este script.
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
    
    
