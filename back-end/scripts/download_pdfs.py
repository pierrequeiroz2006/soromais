import requests
import os

ESTADOS = [
    "paraiba"
]

#URL QUE SERÁ USADO COMO BASE PARA O DOWNLOAD DOS PDFS
URL_BASE = "https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/animais-peconhentos/hospitais-de-referencia/{estado_selecionado}/@@download/file"

os.makedirs("pdfs", exist_ok=True)

#ITERAÇÃO SOB OS ESTADOS PARA DOWNLOAD DE CADA UM DOS PDFS DELES
for estado in ESTADOS:
    
    url = URL_BASE.format(estado_selecionado=estado)  #SUBSTITUIÇÃO DO NOME DO ESTADO NA URL
    response = requests.get(url, timeout=30)          #ACESSA E TENTA BAIXAR O PDF
    
    if response.status_code == 200:                 
        
        with open(f"pdfs/{estado}.pdf", "wb") as f:   #SALVA EM ESCRITA BINÁRIA
            f.write(response.content)
        print(f"✓ {estado.upper()} baixado")
        
    else:
        print(f"✗ {estado.upper()} — status {response.status_code}")   #RETORNA O POSSÍVEL ERRO
    
    
