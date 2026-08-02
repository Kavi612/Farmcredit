# FarmCredit AI — Project Overview

**Audience:** stakeholders, bank/product reviewers, and interviewers evaluating this as an applied AI/ML portfolio project.  
**Status:** Portfolio / educational demonstration — synthetic data only; not a production lending system.

---

## 1. PROJECT SUMMARY

FarmCredit AI helps Indian farmers and rural bank officers understand crop-loan default risk before a lending decision is locked in. Farmers enter farm and loan details (or try a sample profile) and receive a risk score, plain-language explanations of what drove that score, practical advisory text, and a downloadable PDF brief. Bank officers review the same demo applications in a dashboard, filter by risk, and record approve / flag / reject decisions for the session. The project is built to showcase a complete, production-shaped ML + explainability + optional LLM pipeline end to end — not to replace regulated credit systems.

---

## 2. USER WORKFLOW

The live product is a single Streamlit app (`frontend/streamlit_app.py`) with four views: **Welcome**, **Farmer**, **Bank Officer**, and **About**. Navigation is via the site header (Home, About, Bank Officer / Farmer View).

### Welcome

1. User lands on the welcome page (hero, feature cards, “how it works,” and start choices).
2. They can:
   - **Try Demo Data** → Farmer view, demo profile picker  
   - **Enter Your Own Details** → Farmer view, blank assessment form  
   - **Bank Officer →** (header) → Bank Officer dashboard  
   - **About** → project explanation for farmers, banks, and how AI helps  

### Farmer View

1. **Choose path:** Try Demo Data or Enter Your Own Data.
2. **If demo:** Select one of **five** demo farmer profiles (DEMO-01 … DEMO-05). Choosing a profile loads that farmer’s details into the **same shared input form** used for manual entry.
3. **If manual:** Fill the empty form (location, crop, farm, and credit fields — see Features).
4. **Submit** (“Get my risk assessment”) → backend `/assess` (demo profiles typically use precomputed cache; custom inputs run live XGBoost + SHAP).
5. **Results screen shows:**
   - Risk score and risk level (Low / Medium / High / Critical)
   - SHAP-explained top risk drivers (and protective factors where available)
   - AI advisory text (cached demo text, template text, or live LLM when enabled)
   - Downloadable **PDF** report and **JSON** report  
6. User can start a new assessment or switch to Bank Officer / Home / About via the header.

### Bank Officer View

1. Officer opens Bank Officer view (requires the API to be reachable).
2. Dashboard loads the **five demo farmer applications** from the backend.
3. Officer can:
   - Filter by risk level, state, decision status; search by name or ID  
   - View portfolio metrics (applications, pending, approved, rejected, flagged)  
   - View charts: average risk by state, applications by risk band, High/Critical counts by state  
   - Select an application to see narrative and top risk drivers  
   - **Approve**, **Reject**, **Flag**, or reset to Pending (optional note)  
4. Decisions are stored **in the browser session only** (reset clears them). There is no persistent database and no CSV export in the current bank UI.

---

## 3. FEATURES LIST

### Farmer-Facing Features

- Welcome landing with clear paths into demo or custom assessment  
- Try Demo Data: five curated farmer personas spanning Low → Critical risk  
- Enter Your Own Details: full assessment form (state, district/zone, crop, season, soil, irrigation, land size, rainfall, loan amount, income, debt, prior loans, prior default, repayment score, optional name)  
- Shared form for both demo prefill and manual entry  
- Results: risk badge (score and band), recommendations summary, full advisory card  
- PDF and JSON report download  
- Navigation to About and Bank Officer from the farmer flow  

### Risk Prediction & Explainability Features

- XGBoost regression of `default_risk` in \[0, 1\]  
- Risk bands: Low (&lt; 0.25), Medium (&lt; 0.50), High (&lt; 0.75), Critical (≥ 0.75)  
- Live scoring for custom inputs via `/predict-risk` and `/assess`  
- SHAP TreeExplainer: top factors with direction (increases / decreases risk) and plain-language hints  
- Protective factors surfaced where available  
- Precomputed demo cache for instant, consistent DEMO-01 … DEMO-05 assessments  

### AI Advisory Features

- Farmer-facing advisory text covering risk context, practical next steps, and indicative scheme language (e.g. PM-KISAN, KCC, PMFBY — framed as guidance, not eligibility guarantees)  
- Three sources, in priority order: **demo cache** → **live fine-tuned Mistral** (when enabled and requested) → **deterministic template** fallback  
- Advisory metadata in the UI (model source, cached vs live, latency when live)  
- Public/demo path defaults to cache/template (`LLM_ENABLED=false`)  

### Bank Officer Dashboard Features

- Application queue for all five demo farmers  
- Filters: risk level, state, decision (Pending / Approved / Rejected / Flagged), text search  
- Session metrics for the filtered queue  
- Charts: average risk by state, applications by risk band, High/Critical by state  
- Per-application detail: narrative, top drivers, officer note  
- Approve / Reject / Flag / Reset to Pending  
- Reset all decisions for the session  
- Switch back to Farmer View  

*Not implemented in the current bank UI:* CSV/JSON portfolio export, persistent officer accounts, or a larger synthetic queue beyond the five demos.

### Report Generation Features

- JSON risk brief via `/generate-report`  
- Downloadable PDF via ReportLab (`/generate-report/pdf`): summary, risk, SHAP drivers, advisory, schemes, demo disclaimer  
- Farmer UI: prepare and download PDF; download JSON  

### Technical Features

- FastAPI backend with OpenAPI docs (`/docs`)  
- Health endpoint reporting XGBoost / SHAP / LLM load status  
- Orchestrated `/assess` pipeline (predict + explain + advisory + report)  
- Demo farmer catalog and on-disk demo cache  
- Streamlit frontend with responsive header (mobile menu vs desktop links)  
- CORS and `FARMCREDIT_API_URL` for local or remote API  
- Docker image for CPU deployment with LLM off  
- Synthetic data generator, XGBoost train/evaluate pipeline, and demo-cache builder under `ml/`  

---

## 4. TECH STACK

| Technology | Role |
|---|---|
| **Streamlit** | Farmer and bank officer UI, forms, charts, downloads |
| **FastAPI** | Typed HTTP API for risk, explain, advisory, demo, and reports |
| **Pydantic / pydantic-settings** | Request/response schemas and environment configuration |
| **Uvicorn** | ASGI server for the FastAPI app |
| **XGBoost** | Tabular default-risk model (regression on agri-credit features) |
| **SHAP** | TreeExplainer local explanations of each prediction |
| **scikit-learn / pandas / NumPy / joblib** | Data handling, evaluation helpers, model serialization |
| **Mistral-7B-Instruct-v0.3** | Base instruct LLM for advisory generation |
| **QLoRA (PEFT + TRL-style fine-tune; bitsandbytes 4-bit)** | Adapter fine-tuning / 4-bit inference path for advisory (Colab T4–class GPU workflow; adapters loaded from Hugging Face when enabled) |
| **Hugging Face Hub / transformers / accelerate** | Download and run base model + PEFT adapter |
| **ReportLab** | Server-side PDF generation |
| **Docker** | Packaged CPU backend deploy (`LLM_ENABLED=false`) |
| **Render** (target) | Host FastAPI + XGBoost + SHAP |
| **Streamlit Community Cloud** (target) | Host the Streamlit UI |
| **Vercel** (optional) | Static portfolio landing page linking to the live demo |

---

## 5. HOW TO RUN THE PROJECT

### Prerequisites

- Python **3.10 or 3.11** recommended  
- Git  
- Two terminals (backend + frontend)  

### Clone and install

```powershell
cd "C:\Users\Kavirathna\OneDrive\Desktop\resume projects\Frarmcredit"
# or: git clone <your-repo-url> && cd Frarmcredit

python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Lean demo install (recommended for running the app)
pip install -r requirements-demo.txt
pip install streamlit-javascript

# Or fuller backend stack (includes LLM libraries):
# pip install -r backend/requirements.txt
# pip install -r frontend/requirements.txt
```

### Environment variables (names only — never commit secrets)

**Backend** (copy `backend/.env.example` → `backend/.env`):

| Variable | Purpose |
|---|---|
| `APP_ENV` | Environment label |
| `CORS_ORIGINS` | Allowed frontend origins |
| `MODEL_DIR` | Path to XGBoost artifacts |
| `DEMO_FARMERS_PATH` | Demo farmer catalog |
| `DEMO_CACHE_DIR` | Precomputed demo bundles |
| `DEMO_USE_CACHE_BY_DEFAULT` | Prefer demo cache on `/assess` |
| `LLM_ENABLED` | Whether to initialize the Mistral client |
| `HF_TOKEN` | Hugging Face token (private adapter / gated models) |
| `HF_MODEL_ID` | PEFT adapter repo id |
| `HF_BASE_MODEL` | Base instruct model id |
| `LLM_LOAD_IN_4BIT` | 4-bit load for inference |
| `LLM_EAGER_LOAD` | Load LLM at startup vs first request |
| `LLM_MAX_NEW_TOKENS` | Generation length |
| `LLM_TEMPERATURE` | Sampling temperature |

**Frontend:**

| Variable | Purpose |
|---|---|
| `FARMCREDIT_API_URL` | Backend base URL (also settable in Streamlit Cloud **Secrets**) |

### Regenerate data and retrain (optional)

Pre-trained artifacts already ship under `ml/artifacts/model/`. To regenerate:

```powershell
$env:PYTHONPATH = (Get-Location).Path
python -m ml.src.generate_synthetic
python -m ml.src.train
python -m ml.src.evaluate
python -m ml.src.build_demo_cache
```

### Start the backend

```powershell
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = (Get-Location).Path
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Confirm: `http://127.0.0.1:8000/health` and `http://127.0.0.1:8000/docs`.

### Start the Streamlit frontend

```powershell
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = (Get-Location).Path
$env:FARMCREDIT_API_URL = "http://127.0.0.1:8000"
python -m streamlit run frontend/streamlit_app.py
```

Open `http://localhost:8501`.

### What `LLM_ENABLED` changes

| | `LLM_ENABLED=false` (default / public deploy) | `LLM_ENABLED=true` |
|---|---|---|
| Advisory | Demo cache (for DEMO ids) or template text | Live generation from base Mistral + PEFT adapter when requested |
| Hardware | Standard CPU | GPU strongly recommended; HF token/model id required for private adapters |
| Startup | Fast | Slower (model download/load) |
| Risk + SHAP | Always available from the XGBoost artifacts | Same |

---

## 6. HOW TO USE THE APP (for non-technical stakeholders)

### If you are a farmer (or watching a farmer demo)

1. Open the app and choose **Try Demo Data** (fastest) or **Enter Your Own Details**.  
2. For a demo, pick a sample farmer — for example a low-risk Punjab wheat grower or a high-risk rainfed cotton grower. Their details appear in the form automatically.  
3. Submit to get an assessment. You will see:
   - A **risk score and level** (Low → Critical)  
   - **Why** that score happened — factors such as rainfall, irrigation, crop choice, debt, or repayment history explained in plain language  
   - **Advice** on safer practices and government schemes that may be relevant (indicative only)  
   - A **PDF** you can download to keep or share  
4. Try another profile or enter your own numbers to see how the explanation changes.

### If you are a bank officer (or watching an officer demo)

1. Click **Bank Officer** in the header.  
2. Browse the queue of demo applications.  
3. Filter by risk band or state; open an application to see drivers.  
4. Mark **Approve**, **Flag**, or **Reject** (and optionally add a note). Decisions stay for this browser session so you can walk through a review workflow in a meeting — they are not stored in a bank system of record.

### Important for every stakeholder

This is a **demonstration**. Scores and advice illustrate how an AI pipeline could support decisions; they are not formal credit decisions and must not be used to approve or deny real loans.

---

## 7. CURRENT DEPLOYMENT STATUS

| Piece | Hosting approach |
|---|---|
| **Backend API** (FastAPI + XGBoost + SHAP + PDF) | **Render** (Docker or Python web service), CPU |
| **Frontend UI** (Streamlit) | **Streamlit Community Cloud** |
| **Portfolio landing page** (static links) | **Vercel** (optional entry URL) |

- The **ML risk model and SHAP explainability run live on standard CPU** infrastructure in this deployment shape.  
- The **fine-tuned LLM advisory does not run live on free-tier public hosting**. Deployments use `LLM_ENABLED=false`, so advisory text comes from **precomputed demo cache** and/or **template** responses.  
- **Live fine-tuned Mistral + QLoRA adapter inference** is implemented in the codebase and can be demonstrated locally or on **GPU-backed** infrastructure when `LLM_ENABLED=true` and Hugging Face credentials/model id are configured.  
- Exact public URLs should be filled into the README / Vercel landing once each service is live and stable (including cold-start wake-up on free Render).

---

## 8. DATA DISCLOSURE

This project uses **realistic synthetic** agricultural and loan data — **not** real farmer records, bank ledgers, or official NABARD / IMD / ICAR microdata.

| Asset | What it is |
|---|---|
| **~10,000 training rows** | Generated with state/crop/soil priors and correlation rules (rainfall, crop water need, irrigation, loan-to-land/income leverage, repayment history, prior default) |
| **Risk labels** | Derived from a latent stress-style function plus noise so the model learns meaningful structure |
| **Five demo farmers** | Hand-crafted personas with cached scores, SHAP factors, and advisory text |
| **Instruction data for QLoRA** | Template-generated farmer Q&A pairs (~400) for advisory fine-tuning |

The data is designed so explanations and model behavior look agriculturally plausible. It must **not** be cited as official statistics or used for real credit decisions. FarmCredit AI demonstrates a complete ML/LLM engineering pipeline; it is not a production lending product.

---

## 9. RESULTS / MODEL PERFORMANCE

Metrics below are taken from saved artifacts (`ml/artifacts/model/metrics.json`, `train_meta.json`) and demo cache files — not estimates.

### XGBoost (held-out test set, n = 1,500)

| Metric | Value |
|---|---|
| **RMSE** | 0.080 |
| **MAE** | 0.063 |
| **AUC-ROC** (binary @ 0.5) | 0.962 |
| **Accuracy** | 0.891 |
| **Precision** | 0.876 |
| **Recall** | 0.808 |
| **F1** | 0.841 |
| **Band accuracy** (Low/Med/High/Critical) | 0.742 |
| **Validation RMSE** (early stopping) | 0.080 |
| **Best boosting iteration** | 389 (of up to 400 estimators) |

Confusion matrix (binary threshold 0.5): TN = 907, FP = 61, FN = 102, TP = 430.

### QLoRA fine-tuning (as documented in project materials)

| Item | Value |
|---|---|
| Base model | `mistralai/Mistral-7B-Instruct-v0.3` |
| Method | QLoRA / PEFT adapters, 4-bit (bitsandbytes) |
| Instruction examples | ~400 Alpaca-format pairs |
| Final training / eval loss | **Not stored in this repository** (recorded in the training notebook / Hub run, not in committed metrics files) |
| Epochs | **Not recorded in committed project metrics** |

Honesty note: XGBoost metrics are fully reproducible from repo artifacts. LLM fine-tune loss/epoch numbers should be copied from the Colab/Hub training run if needed for interviews; they are not present as saved metric files alongside the XGBoost artifacts.

### Demo farmer risk scores (from demo cache)

| ID | Persona (summary) | Risk level | Score |
|---|---|---|---|
| DEMO-01 | Harpreet Singh — Punjab wheat, canal | **Low** | **0.050** |
| DEMO-02 | Savita Patil — Maharashtra soybean | **Medium** | **0.409** |
| DEMO-03 | Ramesh Jadhav — rainfed cotton | **High** | **0.681** |
| DEMO-04 | Anita Devi — Bihar rice, prior default | **Critical** | **1.000** |
| DEMO-05 | Gopal Sharma — Rajasthan millet + drip | **Medium** | **0.289** |

Demo score range: **0.05 (Low) → 1.00 (Critical)**.

---

## 10. ROADMAP — PLANNED UPGRADES

The following items are **forward-looking and not yet implemented** in the current codebase.

### a) Real Agricultural Data Integration

Replace synthetic training data with governed real datasets from sources such as NABARD, ICAR, IMD, and data.gov.in to move toward production-grade accuracy and credibility.

### b) GPU-Hosted Live LLM in Production

Move the fine-tuned Mistral advisory from cached/template mode to always-on live inference by hosting on GPU-backed infrastructure instead of free-tier CPU hosting.

### c) Persistent Database & Authentication

Replace demo-cache JSON files and session-only officer decisions with a real database (e.g. PostgreSQL) and add authentication for bank officers so applications and decisions persist across sessions.

### d) Multi-language Support

Extend farmer-facing advisory and UI copy to regional Indian languages (e.g. Tamil, Hindi) for the intended user base.

### e) NABARD / RBI Integration Layer

Explore integration points with institutional data and compliance expectations for a production-ready risk-engine variant — beyond the portfolio demo scope.

---

## Closing note for reviewers

FarmCredit AI is an **honest portfolio demonstration**: a working farmer UI, bank officer dashboard, FastAPI services, trained XGBoost model with strong held-out metrics, SHAP explainability, ReportLab PDFs, and an optional QLoRA Mistral advisory path. Public CPU deploys keep the LLM off and use cache/template advisory; live LLM inference is available when hardware and tokens allow. Synthetic data powers the story so the full engineering pipeline can be shown without exposing real farmer or bank records.
