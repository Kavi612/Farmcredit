# FarmCredit AI — FastAPI backend (CPU demo deploy, LLM optional/off)
FROM python:3.11-slim

WORKDIR /app

# System deps for xgboost/shap/matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# App code + ML artifacts + demo data
COPY backend/ backend/
COPY ml/artifacts/model/ ml/artifacts/model/
COPY data/reference/ data/reference/

ENV PYTHONPATH=/app
ENV APP_ENV=production
ENV LLM_ENABLED=false
ENV MODEL_DIR=ml/artifacts/model
ENV DEMO_FARMERS_PATH=backend/app/data/demo_farmers.json
ENV DEMO_CACHE_DIR=backend/app/data/demo_cache

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
