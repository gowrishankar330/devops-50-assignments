# ---- Stage 1: builder (the kitchen) ----
FROM python:3.12 AS builder

WORKDIR /app

COPY requirements.txt .

# --prefix installs everything into one folder we can copy out later
RUN pip3 install --prefix=/install -r requirements.txt

# ---- Stage 2: runtime (the cake) ----
FROM python:3.12-slim

RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# reach into stage 1: grab installed packages, place them where Python looks
COPY --from=builder /install /usr/local

# copy the app code itself (comes from your repo, not the builder)
COPY main.py .

# create a non-root user and switch to it — a container breakout
# from root inside the container is far more dangerous
RUN adduser --disabled-password --gecos "" appuser
USER appuser

EXPOSE 8080

# CMD = what runs when the container STARTS (not during build)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--access-logfile", "main:app"]
