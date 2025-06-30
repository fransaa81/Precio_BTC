# Dockerfile con Python como base para Bitcoin Price Monitor
FROM python:3.11-slim

# Configurar entorno no interactivo  
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema y Chrome
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    tzdata \
    ca-certificates \
    unzip \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Configurar directorio de trabajo
WORKDIR /app

# Copiar requirements primero para cache de Docker
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

# Crear directorio de logs con permisos
RUN mkdir -p /app/logs && chmod 755 /app/logs

# Variables de entorno optimizadas
ENV CHROME_BIN=/usr/bin/google-chrome \
    CHROME_PATH=/usr/bin/google-chrome \
    TZ=America/Argentina/Buenos_Aires \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DISPLAY=:99

# Usuario no-root para seguridad
RUN useradd -m -u 1000 bitcoin && \
    chown -R bitcoin:bitcoin /app

USER bitcoin

# Healthcheck para verificar que el contenedor funciona
HEALTHCHECK --interval=5m --timeout=30s --start-period=2m --retries=3 \
    CMD python -c "import requests; requests.get('https://httpbin.org/get', timeout=10)" || exit 1

# Comando principal que ejecuta el scheduler automático
CMD ["python", "docker_scheduler.py"]
