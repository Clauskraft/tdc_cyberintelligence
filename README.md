# TDC Cyberintelligence System

En åben og modulær cloud-baseret trusselsintelligensplatform, designet til at detektere og analysere danske cyberhændelser med hjælp fra eksterne datakilder. Platformen er containeriseret og kan køre på Cloud Run, Vertex AI eller lokalt.

## Funktionalitet
- Realtidsovervågning af væsentlige danske cyberhændelser.
- Integrerer data fra MISP, OTX, Shodan, HIBP m.m., samt OSINT-tools som SpiderFoot, LeakLooker-X og Oblivion.
- Analyselag med korrelationsanalyse, risikoscore og reguleringsanalyse.
- Produktionsklar REST API (FastAPI) med endpoint til dataindsamling/rapportering og health check.
- Streamlit‑dashboard til visning af rapporter og Mobile‑App med dashboard‑visning.

## Installation

Projektet kræver Python 3.11+ og pip. Clone repoet og installer afhængigheder:

```bash
python3 -m venv venv && source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Lokal kørsel

Kør FastAPI serveren med Uvicorn på port 8000:

```bash
uvicorn tdc_cyberintelligence.api:app --host 0.0.0.0 --port 8000
```

Start Streamlit‑dashboardet i en anden terminal:

```bash
streamlit run tdc_cyberintelligence/dashboard/streamlit_app.py
```

## Cloud Run deployment

Byg og upload containeren til Google Cloud Build og deploy den til Cloud Run:

```bash
gcloud builds submit --tag gcr.io/<PROJECT_ID>/tdc-cyberintelligence

gcloud run deploy tdc-cyberintelligence \
  --image gcr.io/<PROJECT_ID>/tdc-cyberintelligence \
  --platform managed \
  --region europe-north1 \
  --allow-unauthenticated \
  --set-env-vars MISP_URL=...,MISP_KEY=...,OTX_KEY=...,SHODAN_KEY=...,HIBP_KEY=...
```

## API Endpoints

- `GET /health` – Returnerer `{"status": "ok"}` hvis tjenesten er oppe.
- `POST /collect-and-analyze` – Indsamler data fra alle kilder, analyserer dem og genererer en rapport. Rapporten gemmes i mappen `reports/` og returneres som JSON.
- `GET /reports/latest` – Returnerer den senest genererede rapport i JSON-format.

## Mobilapp og Dashboard

Mobilappen henter rapporter fra `/reports/latest` og kan åbne Streamlit‑dashboardet via en WebView. Dashboardet viser et interaktivt overblik over hændelser og IOCs med grafer og tabeller.

## License

Dette projekt er open source (MIT) og kan frit videreudvikles. Husk at overholde licenserne for de eksterne værktøjer og feeds.
