# Etapa 2 do pipeline (back-end/scripts/pipeline.py): lê pdfs/paraiba.pdf (tabela de hospitais
# de referência do Ministério da Saúde) e extrai só a coluna de código CNES de cada linha,
# gravando em scripts/cnes.json. Esse arquivo é a "lista de quem nos interessa" que o
# final_json.py usa para filtrar o CSV gigante do CNES (download_csv.py).
import pdfplumber
import json
from pathlib import Path

BASE = Path(__file__).parent.parent

# Linhas de cabeçalho/repetição de título que aparecem espalhadas nas tabelas do PDF e devem
# ser ignoradas (não são hospitais de verdade).
CABECALHOS = ['PARAÍBA', 'MUNICÍPIO', 'UNIDADE']

cnes_list = []

with pdfplumber.open(BASE / "pdfs/paraiba.pdf") as pdf:
    for page in pdf.pages:
        for table in page.extract_tables():
            for row in table:
                valores = [v for v in row if v is not None]

                # Linha incompleta (menos de 6 colunas preenchidas) não é um registro válido
                if len(valores) < 6:
                    continue
                # Pula linhas de cabeçalho repetidas em cada página do PDF
                if any(h in (valores[1] or '') for h in CABECALHOS):
                    continue

                # A coluna do código CNES é a 5ª coluna não-nula (índice 4) de cada linha da tabela
                cnes = str(valores[4]).replace('\n', ' ').strip()
                if cnes:
                    cnes_list.append({"cnes": int(cnes)})

with open(BASE / "cnes.json", 'w', encoding='utf-8') as f:
    json.dump(cnes_list, f, ensure_ascii=False, indent=2)

print(f"✓ {len(cnes_list)} registros extraídos")