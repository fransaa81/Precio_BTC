# Script de inicialización automática para Bitcoin Price Monitor con Docker
# Versión PowerShell para Windows

param(
    [switch]$Force,
    [switch]$SkipBuild
)

Write-Host "🐳 === BITCOIN PRICE MONITOR - INICIALIZACIÓN AUTOMÁTICA ===" -ForegroundColor Yellow
Write-Host "==============================================================" -ForegroundColor Yellow

# Verificar Docker
try {
    docker --version | Out-Null
    Write-Host "✅ Docker detectado" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Docker no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "ℹ️  Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop" -ForegroundColor Cyan
    exit 1
}

# Verificar que Docker esté ejecutándose
try {
    docker info | Out-Null
    Write-Host "✅ Docker está ejecutándose" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Docker no está ejecutándose" -ForegroundColor Red
    Write-Host "ℹ️  Inicia Docker Desktop" -ForegroundColor Cyan
    exit 1
}

# Verificar docker-compose
$ComposeCmd = "docker-compose"
try {
    docker-compose --version | Out-Null
    Write-Host "✅ Docker Compose detectado" -ForegroundColor Green
} catch {
    try {
        docker compose version | Out-Null
        $ComposeCmd = "docker compose"
        Write-Host "✅ Docker Compose (integrado) detectado" -ForegroundColor Green
    } catch {
        Write-Host "❌ ERROR: Docker Compose no está disponible" -ForegroundColor Red
        exit 1
    }
}

# Verificar archivo .env
if (-not (Test-Path ".env")) {
    Write-Host "❌ ERROR: Archivo .env no encontrado" -ForegroundColor Red
    Write-Host "ℹ️  Copia .env.example a .env y configura tus credenciales" -ForegroundColor Cyan
    exit 1
}
Write-Host "✅ Archivo .env encontrado" -ForegroundColor Green

# Crear directorio de logs
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" -Force | Out-Null
}
Write-Host "✅ Directorio de logs verificado" -ForegroundColor Green

# Detener contenedores existentes
Write-Host "🛑 Deteniendo contenedores existentes..." -ForegroundColor Yellow
try {
    if ($ComposeCmd -eq "docker-compose") {
        docker-compose down --remove-orphans 2>$null
    } else {
        docker compose down --remove-orphans 2>$null
    }
} catch {
    # Ignorar errores si no hay contenedores
}

# Limpiar imágenes anteriores si se especifica
if ($Force) {
    Write-Host "🧹 Limpiando imágenes anteriores..." -ForegroundColor Yellow
    try {
        docker image prune -f --filter label=com.bitcoin.monitor 2>$null
    } catch {
        # Ignorar errores
    }
}

if (-not $SkipBuild) {
    Write-Host ""
    Write-Host "🏗️  CONSTRUYENDO IMAGEN DOCKER..." -ForegroundColor Cyan
    Write-Host "⏳ Esto puede tomar varios minutos la primera vez..." -ForegroundColor Yellow
    
    # Construir la imagen
    try {
        if ($ComposeCmd -eq "docker-compose") {
            docker-compose build --no-cache
        } else {
            docker compose build --no-cache
        }
        Write-Host "✅ Imagen construida exitosamente" -ForegroundColor Green
    } catch {
        Write-Host "❌ ERROR: Falló la construcción de la imagen" -ForegroundColor Red
        Write-Host "ℹ️  Revisa los logs anteriores para más detalles" -ForegroundColor Cyan
        exit 1
    }
}

Write-Host ""
Write-Host "🚀 INICIANDO CONTENEDOR EN MODO AUTOMÁTICO..." -ForegroundColor Cyan

# Iniciar en modo detached (background)
try {
    if ($ComposeCmd -eq "docker-compose") {
        docker-compose up -d
    } else {
        docker compose up -d
    }
    Write-Host "✅ Contenedor iniciado exitosamente" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Falló el inicio del contenedor" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎉 === BITCOIN PRICE MONITOR CONFIGURADO Y EJECUTÁNDOSE ===" -ForegroundColor Green
Write-Host "=============================================================="
Write-Host ""

Write-Host "📊 ESTADO DEL SISTEMA:" -ForegroundColor Cyan
if ($ComposeCmd -eq "docker-compose") {
    docker-compose ps
} else {
    docker compose ps
}

Write-Host ""
Write-Host "📋 INFORMACIÓN IMPORTANTE:" -ForegroundColor Yellow
Write-Host "  • ✅ El sistema está ejecutándose 24/7 automáticamente"
Write-Host "  • ⏰ Enviará reportes DIARIOS a las 9:00 AM (Argentina)"
Write-Host "  • 🔄 Se reinicia automáticamente si hay problemas"
Write-Host "  • 📧 No requiere intervención manual"
Write-Host ""

Write-Host "🔧 COMANDOS ÚTILES:" -ForegroundColor Cyan
Write-Host "  Ver logs en tiempo real:"
Write-Host "    $ComposeCmd logs -f" -ForegroundColor White
Write-Host ""
Write-Host "  Ver estado:"
Write-Host "    $ComposeCmd ps" -ForegroundColor White
Write-Host ""
Write-Host "  Reiniciar:"
Write-Host "    $ComposeCmd restart" -ForegroundColor White
Write-Host ""
Write-Host "  Detener:"
Write-Host "    $ComposeCmd down" -ForegroundColor White
Write-Host ""

# Mostrar logs iniciales
Write-Host "📄 LOGS INICIALES (últimas 20 líneas):" -ForegroundColor Yellow
Write-Host "----------------------------------------"
try {
    if ($ComposeCmd -eq "docker-compose") {
        docker-compose logs --tail=20 bitcoin-monitor
    } else {
        docker compose logs --tail=20 bitcoin-monitor
    }
} catch {
    Write-Host "⏳ Logs aún no disponibles (contenedor iniciando...)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎯 ¡CONFIGURACIÓN COMPLETADA!" -ForegroundColor Green
Write-Host "El sistema ahora funciona completamente automático." -ForegroundColor Green
Write-Host "Los reportes se enviarán diariamente a las 9:00 AM sin intervención manual." -ForegroundColor Green
