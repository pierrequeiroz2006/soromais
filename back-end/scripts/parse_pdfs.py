import pdfplumber
import pandas as pd
import json

COLUNAS = ['municipio', 'unidade_de_saude', 'endereco', 'telefone', 'cnes', 'atendimentos_disponiveis']
 
#STRINGS QUE IDENTIFICAM LINHAS DE CABEÇÃLHO
CABECALHOS = ['PARAÍBA', 'MUNICÍPIO', 'UNIDADE']
 
registros = []
 
with pdfplumber.open("pdfs/paraiba.pdf") as pdf:
    for page in pdf.pages:
        for table in page.extract_tables():
            for row in table:
                #REMOVE COLUNAS NONE
                valores = [v for v in row if v is not None]
 
                #IGNORA LINHAS COM MENOS DE 6 CAMPOS OU CABEÇALHO
                if len(valores) < 6:
                    continue
                if any(h in (valores[1] or '') for h in CABECALHOS):
                    continue
 
                #NORMALIZA QUEBRA DE LINHAS
                valores = [str(v).replace('\n', ' ').strip() if v else '' for v in valores[:6]]
                registros.append(valores)
 
df = pd.DataFrame(registros, columns=COLUNAS)
 
#CNES COMO INTEIRO
df['cnes'] = df['cnes'].apply(lambda x: int(x) if x else None)

#CRIA O CSV PARA MELHOR VISUALIZAÇÃO DOS DADOS E CHECAGEM
df.to_csv('resultado.csv', index=False, sep=';', encoding='utf-8-sig')

#TRANSFORMA O DATAFRAME EM UMA LISTA DE DICIONÁRIOS
hospitais = df.to_dict(orient="records")

#ESCREVE ESSA LISTA NO ARQUIVO
with open('hospitals.json', 'w', encoding='utf-8') as f:
    json.dump(hospitais, f, ensure_ascii=False, indent=2)