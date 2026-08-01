# FarmCredit AI — Deployment Guide

This guide walks through deploying **FarmCredit AI** for a portfolio demo using **Render** (backend API) and **Vercel** (public landing / entry point). The interactive app UI is **Streamlit**, which cannot run on Vercel — it is deployed on **Streamlit Community Cloud** and pointed at your Render API.

---

## What runs where

| Service | Platform | URL example | Role |
|---------|----------|-------------|------|
| **FastAPI backend** | **Render** (Docker) | `https://farmcredit-api.onrender.com` | Risk scoring, SHAP, demo cache, PDF |
| **Streamlit UI** | **Streamlit Cloud** | `https://farmcredit-ai.streamlit.app` | Farmer + bank officer dashboard |
| **Landing page** | **Vercel** (optional) | `https://farmcredit.vercel.app` | Portfolio link, redirects to live demo |

```
User → Vercel landing (optional)
     → Streamlit Cloud (frontend) ──HTTP──► Render (FastAPI + XGBoost)
```

**Recommended demo settings:** `LLM_ENABLED=false` (CPU only, no GPU, no HuggingFace download at startup).

---

## Prerequisites

Before deploying, complete these on your machine:

1. **GitHub account** — both Render and Vercel deploy from Git.
2. **Code pushed to GitHub** — entire repo including:
   - `backend/`
   - `frontend/`
   - `ml/artifacts/model/` (must include trained model files, e.g. `model.joblib` if your loader expects it)
   - `backend/app/data/demo_cache/`
   - `Dockerfile`
3. **Accounts (free tier is fine):**
   - [Render](https://render.com)
   - [Vercel](https://vercel.com)
   - [Streamlit Community Cloud](https://share.streamlit.io) (for the UI)
4. **Do not commit secrets** — no `backend/.env` with real tokens in Git. Use platform env vars / secrets instead.

---

## Part 1 — Deploy the backend on Render

The repo includes a `Dockerfile` that builds the FastAPI app with XGBoost + SHAP artifacts.

### Step 1.1 — Push code to GitHub

```powershell
cd "C:\Users\Kavirathna\OneDrive\Desktop\resume projects\Frarmcredit"
git init
git add .
git commit -m "Prepare FarmCredit AI for deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/farmcredit-ai.git
git push -u origin main
```

Replace `YOUR_USERNAME/farmcredit-ai` with your repository.

### Step 1.2 — Create a Render web service

1. Log in to [dashboard.render.com](https://dashboard.render.com).
2. Click **New +** → **Web Service**.
3. Connect your GitHub account if prompted.
4. Select the **farmcredit-ai** repository.
5. Configure the service:

| Field | Value |
|-------|--------|
| **Name** | `farmcredit-api` (or any name) |
| **Region** | Choose closest to your users (e.g. Singapore / Frankfurt) |
| **Branch** | `main` |
| **Runtime** | **Docker** |
| **Dockerfile path** | `Dockerfile` (repo root) |
| **Instance type** | Free (demo) or Starter (always-on, faster cold starts) |

6. Click **Advanced** and set **Health Check Path** to `/health` (optional but recommended).

### Step 1.3 — Set environment variables on Render

In the Render service → **Environment** tab, add:

| Key | Value |
|-----|--------|
| `APP_ENV` | `production` |
| `LLM_ENABLED` | `false` |
| `MODEL_DIR` | `ml/artifacts/model` |
| `DEMO_FARMERS_PATH` | `backend/app/data/demo_farmers.json` |
| `DEMO_CACHE_DIR` | `backend/app/data/demo_cache` |
| `DEMO_USE_CACHE_BY_DEFAULT` | `true` |
| `CORS_ORIGINS` | `https://YOUR-STREAMLIT-APP.streamlit.app` |

> **Important:** After you deploy Streamlit (Part 2), come back and update `CORS_ORIGINS` with your exact Streamlit URL. You can add multiple origins separated by commas.

Optional (only if you enable live LLM on a GPU host — not for free Render):

| Key | Value |
|-----|--------|
| `HF_TOKEN` | Your HuggingFace token |
| `HF_MODEL_ID` | `your-username/farmcredit-ai-mistral-7b` |
| `LLM_ENABLED` | `true` |

### Step 1.4 — Deploy

1. Click **Create Web Service**.
2. Wait for the Docker build (first deploy may take 5–15 minutes).
3. When status is **Live**, copy your service URL, e.g.  
   `https://farmcredit-api.onrender.com`

### Step 1.5 — Verify the backend

Open in a browser or run:

```powershell
curl https://farmcredit-api.onrender.com/health
```

Expected: JSON with `"status": "ok"` and XGBoost loaded (not `"xgb_loaded": false` with a load error).

Also check API docs:  
`https://farmcredit-api.onrender.com/docs`

### Step 1.6 — Render free-tier notes

- Service **spins down after ~15 minutes** of inactivity.
- First request after idle can take **30–60 seconds** (cold start).
- For interviews, open `/health` once before sharing the demo link, or upgrade to Starter.

---

## Part 2 — Deploy the Streamlit frontend (required)

**Streamlit is a long-running Python server.** It does **not** run on Vercel serverless. Use **Streamlit Community Cloud** (free) for the UI.

### Step 2.1 — Add a root requirements file (if missing)

Streamlit Cloud looks for `requirements.txt` at the repo root. Create or ensure this file exists:

**`requirements.txt`** (repo root):

```text
-r requirements-demo.txt
streamlit-javascript>=0.1.5,<1.0.0
```

Commit and push:

```powershell
git add requirements.txt
git commit -m "Add root requirements for Streamlit Cloud"
git push
```

### Step 2.2 — Create the Streamlit Cloud app

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **New app**.
3. Select your repository and branch (`main`).
4. Set **Main file path:**  
   `frontend/streamlit_app.py`
5. Under **Advanced settings:**
   - **Python version:** 3.11
   - **Secrets:** add (replace with your Render URL):

```toml
FARMCREDIT_API_URL = "https://farmcredit-api.onrender.com"
```

6. Click **Deploy**.

### Step 2.3 — Verify the frontend

1. Open your Streamlit URL, e.g. `https://farmcredit-ai.streamlit.app`.
2. On the welcome page, click **Try Demo Data** → pick **DEMO-01**.
3. You should see risk score, SHAP factors, and advisory text.

If you see connection errors:

- Confirm `FARMCREDIT_API_URL` in Streamlit secrets (no trailing slash).
- Confirm Render `/health` works.
- Update Render `CORS_ORIGINS` with your Streamlit URL and redeploy Render if needed.

### Step 2.4 — Update Render CORS (if not done yet)

Render dashboard → your service → **Environment**:

```
CORS_ORIGINS=https://your-app-name.streamlit.app
```

Save changes → Render will redeploy automatically.

---

## Part 3 — Deploy on Vercel

Vercel is best used here as a **fast portfolio landing page** that links to your **Streamlit demo** and **Render API docs**. The full Streamlit app itself stays on Streamlit Cloud (Part 2).

### Why not the full app on Vercel?

| Component | Vercel? | Reason |
|-----------|---------|--------|
| Streamlit UI | No | Needs a persistent Python process; Vercel is serverless |
| FastAPI + XGBoost + SHAP | Not recommended | Large dependencies, cold starts, size/time limits |
| Static landing + links | **Yes** | Perfect for resume / portfolio entry |

### Step 3.1 — Create a landing folder in the repo

Create this structure:

```text
landing/
├── index.html
└── vercel.json
```

**`landing/index.html`** — minimal portfolio page:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>FarmCredit AI</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 640px; margin: 4rem auto; padding: 0 1rem; }
    h1 { color: #14532d; }
    a.btn {
      display: inline-block; margin: 0.5rem 0.5rem 0.5rem 0;
      padding: 0.75rem 1.25rem; background: #15803d; color: #fff;
      text-decoration: none; border-radius: 8px; font-weight: 600;
    }
    a.btn.secondary { background: #fff; color: #15803d; border: 1px solid #15803d; }
  </style>
</head>
<body>
  <h1>FarmCredit AI</h1>
  <p>AI-powered crop loan default prediction and agricultural advisory for Indian farmers. Portfolio demo — synthetic data only.</p>
  <p>
    <a class="btn" href="https://YOUR-STREAMLIT-APP.streamlit.app">Open live demo</a>
    <a class="btn secondary" href="https://farmcredit-api.onrender.com/docs">API docs</a>
  </p>
  <p><small>Backend: Render · UI: Streamlit Cloud · This page: Vercel</small></p>
</body>
</html>
```

Replace `YOUR-STREAMLIT-APP` and the Render URL with your real URLs.

**`landing/vercel.json`:**

```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

Commit and push:

```powershell
git add landing/
git commit -m "Add Vercel landing page"
git push
```

### Step 3.2 — Import project on Vercel

1. Log in to [vercel.com](https://vercel.com) → **Add New…** → **Project**.
2. Import the same GitHub repository.
3. Configure:

| Field | Value |
|-------|--------|
| **Framework Preset** | Other |
| **Root Directory** | `landing` |
| **Build Command** | (leave empty) |
| **Output Directory** | `.` |

4. Click **Deploy**.

### Step 3.3 — Custom domain (optional)

1. Vercel project → **Settings** → **Domains**.
2. Add your domain (e.g. `farmcredit.yourdomain.com`) and follow DNS instructions.

### Step 3.4 — Verify Vercel deployment

1. Open your Vercel URL, e.g. `https://farmcredit-ai.vercel.app`.
2. Click **Open live demo** → should open Streamlit.
3. Click **API docs** → should open Render Swagger UI.

### Step 3.5 — Optional: redirect root domain to Streamlit

If you want Vercel to skip the landing page and redirect straight to Streamlit, use this **`landing/vercel.json`** instead:

```json
{
  "redirects": [
    {
      "source": "/",
      "destination": "https://YOUR-STREAMLIT-APP.streamlit.app",
      "permanent": false
    }
  ]
}
```

Redeploy on Vercel after changing the file.

---

## Environment variables — full reference

### Render (backend)

| Variable | Required | Example |
|----------|----------|---------|
| `LLM_ENABLED` | Yes | `false` |
| `APP_ENV` | Yes | `production` |
| `MODEL_DIR` | Yes | `ml/artifacts/model` |
| `DEMO_CACHE_DIR` | Yes | `backend/app/data/demo_cache` |
| `DEMO_FARMERS_PATH` | Yes | `backend/app/data/demo_farmers.json` |
| `CORS_ORIGINS` | Yes | Streamlit app URL |
| `HF_TOKEN` | Only if LLM on | — |

### Streamlit Cloud (frontend secrets)

| Variable | Required | Example |
|----------|----------|---------|
| `FARMCREDIT_API_URL` | Yes | `https://farmcredit-api.onrender.com` |

### Vercel (landing)

No secrets required for the static landing page. URLs are hardcoded in `index.html`.

---

## Post-deploy checklist

- [ ] Render `/health` returns OK with model loaded
- [ ] Render `/docs` loads Swagger UI
- [ ] Streamlit app loads and **Try Demo Data** works
- [ ] PDF download works on a demo farmer result
- [ ] Bank Officer dashboard loads 5 demo farmers
- [ ] `CORS_ORIGINS` on Render includes Streamlit URL
- [ ] Vercel landing links point to correct Streamlit + API URLs
- [ ] README updated with live demo links

Update **`README.md`** demo table:

```markdown
| **Live demo** | https://your-app.streamlit.app |
| **Portfolio entry** | https://your-project.vercel.app |
| **API docs** | https://farmcredit-api.onrender.com/docs |
```

---

## Troubleshooting

### Backend: `xgb_loaded: false` or model error on `/health`

- Ensure `ml/artifacts/model/` contains all required files (check `backend/app/ml/risk_model.py` for expected filenames).
- Confirm files are committed to Git (not excluded by `.gitignore`).
- Rebuild Render service after pushing model artifacts.

### Frontend: “Cannot connect to API” / timeout

- Check `FARMCREDIT_API_URL` in Streamlit secrets (HTTPS, no trailing slash).
- Wake Render: visit `/health` and wait for cold start to finish.
- Check Render logs: dashboard → service → **Logs**.

### CORS errors in browser

- Add exact Streamlit origin to Render `CORS_ORIGINS`:
  `https://your-app.streamlit.app`
- Redeploy Render after changing env vars.

### Streamlit build fails

- Ensure root `requirements.txt` exists and includes `streamlit-javascript`.
- Set Python 3.11 in Streamlit Cloud advanced settings.
- Check build logs for missing packages.

### Vercel shows 404

- Confirm **Root Directory** is set to `landing`.
- Confirm `index.html` exists inside `landing/`.

---

## Local vs production quick reference

| | Local | Production |
|---|--------|--------------|
| Backend | `http://127.0.0.1:8000` | `https://farmcredit-api.onrender.com` |
| Frontend | `http://localhost:8501` | `https://your-app.streamlit.app` |
| Landing | — | `https://your-project.vercel.app` |
| Set API URL | `$env:FARMCREDIT_API_URL="http://127.0.0.1:8000"` | Streamlit secrets / Render env |

**Local run (two terminals):**

```powershell
# Terminal 1 — backend
cd "C:\Users\Kavirathna\OneDrive\Desktop\resume projects\Frarmcredit"
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = (Get-Location).Path
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000

# Terminal 2 — frontend
cd "C:\Users\Kavirathna\OneDrive\Desktop\resume projects\Frarmcredit"
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = (Get-Location).Path
$env:FARMCREDIT_API_URL = "http://127.0.0.1:8000"
python -m streamlit run frontend/streamlit_app.py
```

---

## Optional: enable live LLM in production

Not recommended on Render free tier (no GPU, large download). If you deploy on a GPU host (RunPod, Lambda Labs, etc.):

1. Set `LLM_ENABLED=true`
2. Set `HF_TOKEN` and `HF_MODEL_ID`
3. Expect long startup and higher cost
4. Demo cache + template advisory still work with `LLM_ENABLED=false` for portfolio demos

---

## Summary

| Step | Platform | What you deploy |
|------|----------|-----------------|
| 1 | **Render** | FastAPI + XGBoost + SHAP (Docker) |
| 2 | **Streamlit Cloud** | Streamlit UI (farmer + bank views) |
| 3 | **Vercel** | Static landing page linking to demo + API |

This is the standard layout for this project: **Render for the API**, **Streamlit Cloud for the app**, **Vercel for a clean portfolio URL**.
