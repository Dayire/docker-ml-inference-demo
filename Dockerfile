# Dependencies first: editing Python code will not reinstall these packages.
FROM python:3.11-slim-bookworm
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 MAX_CHARS=200 MODEL_PATH=/app/models/sentiment.joblib
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY pyproject.toml .
COPY src ./src
RUN pip install --no-cache-dir --no-deps .
# Tiny, deterministic model for class. Real deployments copy a trained artifact.
RUN python -m text_inference.train
COPY smoke_test.py .
EXPOSE 8000
CMD ["python", "smoke_test.py"]
