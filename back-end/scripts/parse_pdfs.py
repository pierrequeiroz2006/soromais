import pdfplumber
import json

CABECALHOS = ['PARAÍBA', 'MUNICÍPIO', 'UNIDADE']

cnes_list = []

with pdfplumber.open("pdfs/paraiba.pdf") as pdf:
    for page in pdf.pages:
        for table in page.extract_tables():
            for row in table:
                valores = [v for v in row if v is not None]

                if len(valores) < 6:
                    continue
                if any(h in (valores[1] or '') for h in CABECALHOS):
                    continue

                cnes = str(valores[4]).replace('\n', ' ').strip()
                if cnes:
                    cnes_list.append({"cnes": int(cnes)})

with open('cnes.json', 'w', encoding='utf-8') as f:
    json.dump(cnes_list, f, ensure_ascii=False, indent=2)