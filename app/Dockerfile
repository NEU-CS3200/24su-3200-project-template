FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y \
  build-essential \
  libfreetype6-dev \
  pkg-config \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY ./src/requirements.txt .
RUN python -m venv /venv && /venv/bin/pip install --no-cache-dir -r requirements.txt

# --- final stage ---
FROM python:3.11-slim

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

WORKDIR /appcode
COPY ./src .

EXPOSE 8501
CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
