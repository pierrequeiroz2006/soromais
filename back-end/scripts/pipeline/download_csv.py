# Etapa 1b do pipeline (back-end/scripts/pipeline.py): baixa o dump público do CNES
# (Cadastro Nacional de Estabelecimentos de Saúde) — um ZIP grande com um CSV de TODOS os
# estabelecimentos de saúde do Brasil — extrai em data/raw/ e apaga o ZIP. Esse CSV é depois
# cruzado em final_json.py com os códigos CNES extraídos do PDF (parse_pdfs.py) para filtrar
# só os hospitais que interessam.
import requests
from pathlib import Path
import zipfile

#URL QUE SERÁ USADO COMO BASE PARA O DOWNLOAD DO CSV
URL_BASE = "https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/CNES/cnes_estabelecimentos_csv.zip"

BASE = Path(__file__).parent.parent
path_raw = BASE / "data/raw"
path_raw.mkdir(parents=True, exist_ok=True)
path_zip = path_raw / "cnes_estabelecimentos.zip"

response = requests.get(URL_BASE, timeout=120)          #ACESSA E TENTA BAIXAR O PDF
    
if response.status_code == 200:                 
        
    with open(path_zip, "wb") as f:
        f.write(response.content)

    with zipfile.ZipFile(path_zip, 'r') as zip_ref:
        zip_ref.extractall(path_raw)

    path_zip.unlink()

    print("✓ CSV baixado e extraído")

else:
    print(f"✗ Falha no download — status {response.status_code}")   #RETORNA O POSSÍVEL ERRO
    

