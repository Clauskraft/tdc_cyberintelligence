# TDC Erhverv – Cyber Intelligence Platform
[![Test Pipeline](https://github.com/tdc_cyberintelligence/tdc_cyberintelligence/actions/workflows/tests.yml/badge.svg)](https://github.com/tdc_cyberintelligence/tdc_cyberintelligence/actions/workflows/tests.yml)

Dette repository indeholder en modulær, cloud‑klar trusselsinformationsplatform, der kombinerer OSINT, teknisk threat intelligence og forretningskritiske analyser målrettet danske virksomheder.

## 🔍 Funktioner

- **Indsamling af IOCs fra OTX, Shodan, Have I Been Pwned (HIBP) og andre kilder** via et plugin‑baseret arkitektur.
- **Realtidsanalyse og berigelse** af trusselsdata gennem analyser som risikoscore.
- **Executive briefings** med KPI’er og sektorspecifikke anbefalinger.
- **Cloud‑klar backend** (FastAPI) kompatibel med Google Cloud Run og BigQuery.
- **Mobilapp og dashboard** (Streamlit) klar til integration.

## 🦋 Arkitektur

```
Data Sources → Collectors → Analyzers → Briefing Engine → Renderers → API (FastAPI)
```

## Komponenter

1. **Data Sources**: Plugin‑moduler henter IoC’er og trusselsdata fra eksterne feeds som OTX og egne OSINT‑værktøjer.
2. **Collectors**: `IOCCollector` samler og deduplikerer data på tværs af kilder.
3. **Analyzers**: Moduler som `CorrelationAnalyzer` og `RiskScoringAnalyzer` beriger data og beregner risikoniveau.
4. **Briefing Engine**: Genererer strukturerede intel‑dokumenter og executive briefings.
5. **Renderers**: Konverterer rapporter til markdown eller HTML; Streamlit præsenterer dem som dashboards.
6. **API**: FastAPI‑baseret service eksponerer endpoints til indsamling, analyse og hentning af rapporter.

## 🚀 Deployment (Google Cloud Run)

1. Installer og auth Google Cloud CLI:
   ```bash
   gcloud auth login
   gcloud config set project <YOUR_PROJECT_ID>
   ```
2. Byg containeren:
   ```bash
   gcloud builds submit --tag gcr.io/<YOUR_PROJECT_ID>/tdc-cyberintelligence .
   ```
3. Deploy til Cloud Run:
   ```bash
  gcloud run deploy tdc-cyberintelligence \
    --image gcr.io/<YOUR_PROJECT_ID>/tdc-cyberintelligence \
    --region <REGION> \
    --allow-unauthenticated \
    --set-secrets OTX_KEY=OTX_KEY:latest,SHODAN_KEY=SHODAN_KEY:latest,HIBP_KEY=HIBP_KEY:latest \
    --set-env-vars BQ_PROJECT=<YOUR_PROJECT_ID>,BQ_DATASET=tdc_intel,BQ_TABLE=threat_indicators
  ```
Note: Udelad variabler for datakilder, du ikke bruger.

## 🔐 Secret Manager

Opret secrets i Google Secret Manager, så API-nøgler ikke hardcodes i deployment:

```bash
gcloud secrets create OTX_KEY --replication-policy="automatic"
echo -n "<OTX_KEY>" | gcloud secrets versions add OTX_KEY --data-file=-
```

Gentag for `SHODAN_KEY` og `HIBP_KEY`, og brug derefter `--set-secrets` som vist ovenfor under deployment.
## 📊 BigQuery-integration

1. Opret dataset:
   ```bash
   bq mk --dataset --location=<REGION> <YOUR_PROJECT_ID>:tdc_intel
   ```
2. Opret tabel:
   ```bash
   bq mk --table \
   --schema indicator:STRING,type:STRING,source:STRING,confidence:STRING,timestamp:TIMESTAMP \
   <YOUR_PROJECT_ID>:tdc_intel.threat_indicators
   ```
   eller brug `bigquery_schema.json`:
   ```bash
   bq mk --table <YOUR_PROJECT_ID>:tdc_intel.threat_indicators ./bigquery_schema.json
   ```

## ⚙️ Automatisering

Du kan oprette et Cloud Scheduler-job til at køre indsamling og analyse regelmæssigt:
```bash
gcloud scheduler jobs create http run-collector-job \
  --schedule="0 6 * * *" \
  --http-method=POST \
  --uri=https://<SERVICE_URL>/collect-and-analyze \
  --time-zone="Europe/Copenhagen"
```

---
