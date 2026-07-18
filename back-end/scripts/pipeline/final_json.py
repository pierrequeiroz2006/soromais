# Etapa 3 (final) do pipeline (back-end/scripts/pipeline.py): cruza a lista de códigos CNES
# extraída do PDF (cnes.json, gerado por parse_pdfs.py) com o CSV público do CNES (baixado por
# download_csv.py) para obter os dados completos (endereço, telefone, geolocalização, etc.) só
# dos hospitais de referência. O resultado é gravado em data/output/hospitais.json, que é o
# arquivo que o seed.py lê para popular a tabela "hospital" no Supabase.
import pandas as pd
from pathlib import Path

BASE = Path(__file__).parent.parent

path_csv = BASE / "data/raw/cnes_estabelecimentos.csv"
path_json = BASE / "cnes.json"
path_result = BASE / "data/output/hospitais.json"

colunas = [
    'CO_CNES',
    'NO_FANTASIA',
    'NU_LATITUDE',
    'NU_LONGITUDE',
    'NU_TELEFONE',
    'NO_LOGRADOURO',
    'NU_ENDERECO',
    'NO_BAIRRO',
    'NO_EMAIL'
]

#Leitura do CSV(SUS) e transformando CO_CNES em str para melhor análise, pois há possibildiade de começo com 0
df_csv = pd.read_csv(path_csv
                   ,sep=";"
                   ,encoding="iso-8859-1"
                   ,dtype={'CO_CNES': str}
                   ,usecols=colunas)

#Leitura do JSON gerado pelo parse do pdf
df_json = pd.read_json(path_json)
df_json['cnes'] = df_json['cnes'].astype(str)

#Cruzamento de dados do CNES para filtrar o CSV enorme
df_result = pd.merge(
    df_json,
    df_csv,
    left_on='cnes',
    right_on='CO_CNES',
    how='inner'
)

#Deletando coluna duplicada do CNES e renomeando CO_CNES
df_result = df_result.drop('CO_CNES', axis=1)

# Diferente de open(), df.to_json() não cria os diretórios do caminho automaticamente —
# sem isso, falha com "Cannot save file into a non-existent directory" na primeira execução.
path_result.parent.mkdir(parents=True, exist_ok=True)

df_result.to_json(path_result
                  ,indent=2
                  ,force_ascii=False
                  ,orient='records')

print(f"✓ {len(df_result)} hospitais exportados")



