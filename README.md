# TDC Erhverv – Cyber Intelligence Platform

Dette repository indeholder en modulær, cloud‑klar trusselsinformationsplatform, der kombinerer OSINT, teknisk threat intelligence og forretningskritiske analyser målrettet danske virksomheder.

## 🐍 Funktioner

- **Indsamling af IOCs** fra MISP, OTX, Shodan, Have I Been Pwned (HIBP) og andre kilder via et plugin‑baseret arkitektur.
- **Realtidsanalyse og berigelse** af trusselsdata gennem korrelation og risikoscore.
- **Executive briefings** med KPI’er og sektorspecifikke anbefalinger.
- **Cloud‑klar backend** (FastAPI) kompatibel med Google Cloud Run og BigQuery.
- **Mobilapp og dashboard** (Streamlit) klar til integration.

## 📋 Arkitektur

```
Data Sources → Collectors → Analyzers → Briefing Engine → Renderers → API (FastAPI)
```

1. **Data Sources**: Plugin‑moduler henter IoC’er og trusselsdata fra eksterne feeds som MISP, OTX og egne OSINT‑værktøjer.
2. **Collectors**: `IOCCollector` samler og deduplikerer data på tværs af kilder.
3. **Analyzers**: Moduler som `CorrelationAnalyzer` og `RiskScoringAnalyzer` beriger data og beregner risikoniveau.
4. **Briefing Engine**: Genererer strukturerede intel‑dokumenter og executive briefings.
5. **Renderers**: Konverterer rapporter til markdown eller HTML; Streamlit viser dem som dashboards.
6. **API**: FastAPI‑baseret service eksponerer endpoints til indsamling, analyse og hentning af rapporter.

## 🚀 Deployment på Google Cloud Run

1. **Forbered miljø**
   ```bash
   # Log ind i Google Cloud
   gcloud auth login
   gcloud config set project <YOUR_PROJECT_ID>
   ```
2. **Byg containeren**
   ```bash
   # Kør fra projektets rodmappe
   gcloud builds submit --tag gcr.io/<YOUR_PROJECT_ID>/tdc-cyberintelligence .
   ```
3. **Deploy til Cloud Run**
   ```bash
   gcloud run deploy tdc-cyberintelligence \
     --image gcr.io/<YOUR_PROJECT_ID>/tdc-cyberintelligence \
     --region europe-north1 \
     --allow-unauthenticated \
     --set-env-vars MISP_URL=<url>,MISP_KEY=<key>,OTX_KEY=<key>,SHODAN_KEY=<key>,HIBP_KEY=<key>
   ```
   Efter deploy får du en URL (f.eks. `https://tdc-cyberintelligence-xxxx-ew.a.run.app`). Endpoints:
   - `GET /health` → `{"status": "ok"}` for at teste tjenesten.
   - `POST /collect-and-analyze` → Trigger datainhentning og analyse.
   - `GET /reports/latest` → Hent seneste intel‑rapport som JSON.

4. **Scheduler (valgfrit)**
   Opret et Cloud Scheduler‑job via Google Cloud Console til at sende POST‑requests til `/collect-and-analyze` i det ønskede interval (f.eks. dagligt).

## 📊 BigQuery‑integration

Plattformen kan eksportere analyseresultater til BigQuery for videre analyse og dashboarding.

1. **Opret dataset** (erstatter `<YOUR_PROJECT_ID>` med dit projektnavn):
   ```bash
   bq mk --dataset --location=europe-north1 <YOUR_PROJECT_ID>:tdc_intel
   ```
2. **Opret tabel** til trusselsindikatorer:
   ```bash
   bq mk --table \
   --schema indicator:STRING,type:STRING,source:STRING,confidence:STRING,timestamp:TIMESTAMP \
   <YOUR_PROJECT_ID>:tdc_intel.threat_indicators
   ```
   Du kan også definere skemaet i en JSON-fil (se `bigquery_schema.json`) og bruge `--schema=bigquery_schema.json`.

3. **Indsæt data**
   Tilføj kode i dine analysemoduler til at gemme IoC’er i BigQuery via `google-cloud-bigquery`‑klienten eller kør `bq insert`.

## 📱 Mobilapp og dashboard

- **Streamlit Dashboard**: Kør lokalt med `streamlit run tdc_cyberintelligence/dashboard/streamlit_app.py` eller deploy til Cloud Run. Dashboardet viser rapporter og grafer.
- **Android‑app**: Appen henter JSON‑rapporter fra `/reports/latest` og viser dem. WebView indlæser Streamlit‑dashboardet. Tilpas URL’er i `DashboardActivity.kt` til din Cloud Run‑instans.

## 📂 Projektsstruktur

```
tdc_cyberintelligence/
├── api.py                  # FastAPI‑service
├── requirements.txt        # Python‑afhængigheder
├── Dockerfile              # Containerdefinition
├── collectors/
│   ├── __init__.py
│   ├── base_collector.py
│   └── ioc_collector.py
├── analyzers/
│   ├── __init__.py
│   ├── base_analyzer.py
│   ├── correlation_analyzer.py
│   ├── risk_scoring_analyzer.py
│   └── regulatory_analyzer.py
├── sources/                # Kildemoduler (MISP, OTX, osv.)
├── briefing/
│   ├── __init__.py
│   ├── intel_reporter.py
│   ├── executive_briefing.py
│   └── markdown_renderer.py
├── dashboard/              # Streamlit‑app
│   └── streamlit_app.py
├── scheduler/              # Scheduler-scripts
│   └── scheduler.py
└── webhooks/               # Notifiers (Slack, Teams)
    ├── slack_notifier.py
    └── teams_notifier.py
```

## 🔒 Licens og ansvar

Dette projekt bruger open source‑komponenter (MISP, OTX m.fl.) under deres respektive licenser. Anvendelse af data fra dark web, leaks og andre kilder skal ske i henhold til gældende lovgivning og virksomhedens sikkerhedspolitikker.
