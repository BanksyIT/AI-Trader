# Dockerfile
# ----------
# Container setup for full AI trading bot (backend + Streamlit frontend)

FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y build-essential && \
    pip install --upgrade pip && \
    pip install -r backend/requirements.txt && \
    pip install streamlit

EXPOSE 8501

CMD ["streamlit", "run", "frontend/dashboard/app.py"]
