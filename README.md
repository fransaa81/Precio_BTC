# 🪙 Bitcoin Price Monitor - Docker Automatizado

Sistema completamente automatizado que obtiene el precio de Bitcoin de CoinGecko y envía reportes diarios por email usando Docker.

## 🎯 **CARACTERÍSTICA PRINCIPAL: 100% AUTOMATIZADO**

- ✅ **Ejecuta automáticamente diariamente a las 9:00 AM (Argentina)**
- ✅ **No requiere intervención manual**
- ✅ **Se reinicia automáticamente si hay problemas**
- ✅ **Funciona 24/7 en segundo plano**
- ✅ **Scraping en tiempo real de CoinGecko**
- ✅ **Emails HTML con información detallada**

## ⚙️ **CONFIGURACIÓN RÁPIDA**

### 1. Configurar credenciales

Edita el archivo `.env` con tus credenciales:

```env
# Variables de configuración para Zoho Mail
ZOHO_EMAIL=tu_email@zoho.com
ZOHO_PASSWORD=tu_password_de_aplicacion
ZOHO_SMTP_SERVER=smtp.zoho.com
ZOHO_SMTP_PORT=587

# Emails de destino (separados por coma)
RECIPIENT_EMAILS=destinatario1@email.com,destinatario2@email.com

# Configuración del navegador
HEADLESS_MODE=true
WEBDRIVER_TIMEOUT=30

# Zona horaria
TIMEZONE=America/Argentina/Buenos_Aires
```

### 2. Iniciar automáticamente

**Windows (PowerShell):**
```powershell
.\start-automated.ps1
```

**Linux/Mac:**
```bash
./start-automated.sh
```

**Manual:**
```bash
docker-compose up -d
```

## 🚀 **¡LISTO! Sistema funcionando automáticamente**

Una vez iniciado, el sistema:

- 🔄 **Se ejecuta en segundo plano permanentemente**
- ⏰ **Envía reportes DIARIOS a las 9:00 AM automáticamente**
- 📧 **No necesitas hacer nada más**
- 🔧 **Se reinicia solo si hay problemas**

## 📋 **COMANDOS ÚTILES**

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver estado
docker-compose ps

# Reiniciar
docker-compose restart

# Detener
docker-compose down

# Ver logs específicos
docker-compose logs bitcoin-monitor
```

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### Si Docker no puede construir la imagen:

1. **Verificar conectividad:**
   ```bash
   docker run --rm alpine:latest ping -c 3 google.com
   ```

2. **Usar imagen local:**
   - Cambiar `FROM alpine:3.18` por `FROM ubuntu:20.04` en Dockerfile
   - O usar una imagen que ya tengas localmente

3. **Configurar mirror de Docker:**
   ```json
   // En Docker Desktop → Settings → Docker Engine
   {
     "registry-mirrors": ["https://mirror.gcr.io"]
   }
   ```

### Si el contenedor no se inicia:

```bash
# Ver logs detallados
docker-compose logs bitcoin-monitor

# Verificar archivo .env
cat .env

# Reiniciar Docker Desktop
```

## 📊 **MONITOREO**

El sistema incluye:

- ✅ **Healthcheck automático** cada 5 minutos
- ✅ **Logs detallados** en `./logs/`
- ✅ **Restart policy** `unless-stopped`
- ✅ **Logging de estado** cada hora

## 🎉 **RESULTADO**

Una vez configurado, recibirás automáticamente emails diarios con:

- 📈 **Precio actual de Bitcoin**
- 📊 **Cambio en 24h**
- 📉 **Rango de precios del día**
- ⏰ **Timestamp de obtención**
- 🌐 **Fuente de datos (CoinGecko)**

**¡Sin necesidad de ejecutar manualmente nunca más!** 🎯
