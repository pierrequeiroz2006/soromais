# Orquestra o pipeline completo que gera back-end/scripts/data/output/hospitais.json,
# consumido depois por seed.py para popular a tabela "hospital" no Supabase.
#
# Etapas (nessa ordem):
#   1. download_pdfs.py  -> baixa o PDF de hospitais de referência (gov.br) para pdfs/paraiba.pdf
#      download_csv.py   -> baixa e extrai o CSV de estabelecimentos do CNES em data/raw/
#      (essas duas rodam em paralelo, pois são downloads independentes)

#   2. parse_pdfs.py     -> lê pdfs/paraiba.pdf e extrai a lista de códigos CNES -> scripts/cnes.json

#   3. final_json.py     -> cruza cnes.json com o CSV do CNES e gera data/output/hospitais.json
#
# 
# Se já existir um PDF/CSV baixado manualmente, o script pergunta se quer reaproveitá-lo em vez de baixar de novo.

import subprocess
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

BASE = Path(__file__).parent / "pipeline"
ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}


def rodar(script):
    nome = script.replace(".py", "")
    print(f"\n  → {nome:<20} iniciando...")

    result = subprocess.run([sys.executable, BASE / script], capture_output=True, text=True, encoding='utf-8', env=ENV)

    for linha in result.stdout.strip().splitlines():
        print(f"       {linha}")

    if result.returncode != 0:
        raise RuntimeError(f"Erro em {script}:\n{result.stderr}")

    print(f"  ✓ {nome:<20} concluído")


print("\n========== PIPELINE ==========")

# Etapa 1a: PDF de hospitais de referência. Se já existe um arquivo local (baixado manualmente,
# já que a fonte no gov.br exige login), oferece reaproveitá-lo em vez de tentar baixar de novo.

path_pdf = BASE.parent / "pdfs/paraiba.pdf"
usar_pdf_existente = False

if path_pdf.exists():
    resposta = input(f"\nJá existe um PDF em pdfs/{path_pdf.name}. Deseja usá-lo em vez de baixar novamente? (s/n) ").strip().lower()
    usar_pdf_existente = resposta == "s"

# Etapa 1b: CSV de estabelecimentos do CNES (arquivo público, mas grande e demorado de baixar).
path_csv = BASE.parent / "data/raw/cnes_estabelecimentos.csv"
usar_csv_existente = False

if path_csv.exists():
    resposta = input(f"\nJá existe um CSV em data/raw/{path_csv.name}. Deseja usá-lo em vez de baixar novamente? (s/n) ").strip().lower()
    usar_csv_existente = resposta == "s"

# Monta a lista de downloads que realmente precisam rodar e dispara em paralelo.
tarefas = []
if not usar_pdf_existente:
    tarefas.append("download_pdfs.py")
else:
    print("  → download_pdfs       pulado, usando PDF já existente")

if not usar_csv_existente:
    tarefas.append("download_csv.py")
else:
    print("  → download_csv        pulado, usando CSV já existente")

with ThreadPoolExecutor(max_workers=2) as executor:
    futures = {executor.submit(rodar, script): script for script in tarefas}

    for future in as_completed(futures):
        future.result()

# Etapa 2: extrai os códigos CNES do PDF -> scripts/cnes.json

rodar("parse_pdfs.py")
# Etapa 3: cruza cnes.json com o CSV do CNES -> data/output/hospitais.json (entrada do seed.py)

rodar("final_json.py")

# cnes.json é só um artefato intermediário entre as etapas 2 e 3, não precisa sobrar no disco

(BASE.parent / "cnes.json").unlink(missing_ok=True)

print("\n========== CONCLUÍDO ==========\n")
