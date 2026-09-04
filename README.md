# SoroMais

Aplicação web que orienta vítimas de acidentes com animais peçonhentos. A partir da geolocalização do usuário, sugere os hospitais da rede PESA (Pontos Estratégicos de Soro Antiofídico) mais próximos, calcula a rota até o local e envia antecipadamente ao hospital um relatório do caso, agilizando o atendimento antes mesmo da chegada do paciente.

## Diferenciais e Pontos Fortes

- Identificação de espécie por foto usando IA (Gemini), com retorno de gravidade, efeitos do veneno, tempo de ação e condutas de primeiros socorros específicas para o animal identificado.
- Busca de hospitais PESA mais próximos via geolocalização, com cálculo de distância direto no banco (PostGIS) e visualização da rota no mapa.
- Envio antecipado do relatório do caso ao hospital via WhatsApp (Twilio), incluindo PDF gerado automaticamente com os dados do paciente, espécie e gravidade — reduz o tempo de resposta da equipe médica.
- Fluxo pensado para emergência: poucos passos entre identificar o animal, localizar o hospital e notificar a equipe.
- PWA: instalável e utilizável como aplicativo no celular.

## Instalação e Uso Rápido

### Backend

```bash
cd back-end
pip install -r requirements.txt
uvicorn main:app --reload
```

Crie um arquivo `.env` em `back-end/`:

```env
SUPABASE_URL=
SUPABASE_KEY=
GEMINI_API_KEY=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_WHATSAPP_NUMBER=
```

### Frontend

```bash
cd front-end
npm install
npm run dev
```

Crie um arquivo `.env` em `front-end/`:

```env
VITE_API_URL=http://localhost:8000
```

## Estrutura do Banco de Dados

Banco PostgreSQL (Supabase) com extensão PostGIS para cálculo de distância geográfica.

- **bixo** — animais peçonhentos cadastrados (nome, efeitos do veneno, foto).
- **hospital** — unidades PESA (nome, endereço, telefone, email, cnes, coordenadas `lat`/`lng` e ponto geográfico `location` para busca por proximidade).
- **local** — local do incidente (coordenadas, ponto de referência, se é urbano ou rural).
- **paciente** — registro do caso, com chaves estrangeiras para `bixo` (animal envolvido) e `local` (local da picada), além de dados clínicos (idade, peso, tempo decorrido, estado do paciente).

```
bixo ──< paciente >── local
```

## Tecnologias Utilizadas

**Frontend:** React, Vite, React Router, Tailwind CSS, Leaflet / React-Leaflet, PWA

**Backend:** FastAPI, Python, Google Gemini (identificação de espécies), Twilio (WhatsApp), ReportLab (geração de PDF), Geopy

**Banco de Dados:** Supabase (PostgreSQL + PostGIS)
