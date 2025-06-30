#!/usr/bin/env bash
# Script de inicialización automática para Bitcoin Price Monitor con Docker
# Este script configura todo automáticamente sin intervención manual

set -e

echo "🐳 === BITCOIN PRICE MONITOR - INICIALIZACIÓN AUTOMÁTICA ==="
echo "=============================================================="

# Verificar que Docker esté instalado y funcionando
if ! command -v docker &> /dev/null; then
    echo "❌ ERROR: Docker no está instalado"
    echo "ℹ️  Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "❌ ERROR: Docker no está ejecutándose"
    echo "ℹ️  Inicia Docker Desktop"
    exit 1
fi

echo "✅ Docker detectado y funcionando"

# Verificar que docker-compose esté disponible
if ! command -v docker-compose &> /dev/null; then
    echo "⚠️  docker-compose no encontrado, usando docker compose"
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

echo "✅ Docker Compose disponible"

# Verificar archivo .env
if [ ! -f ".env" ]; then
    echo "❌ ERROR: Archivo .env no encontrado"
    echo "ℹ️  Copia .env.example a .env y configura tus credenciales"
    exit 1
fi

echo "✅ Archivo .env encontrado"

# Crear directorio de logs
mkdir -p logs
echo "✅ Directorio de logs creado"

# Detener contenedores existentes si los hay
echo "🛑 Deteniendo contenedores existentes..."
$COMPOSE_CMD down --remove-orphans 2>/dev/null || true

# Limpiar imágenes anteriores
echo "🧹 Limpiando imágenes anteriores..."
docker image prune -f --filter label=com.bitcoin.monitor 2>/dev/null || true

echo ""
echo "🏗️  CONSTRUYENDO IMAGEN DOCKER..."
echo "⏳ Esto puede tomar varios minutos la primera vez..."

# Construir la imagen
if $COMPOSE_CMD build --no-cache; then
    echo "✅ Imagen construida exitosamente"
else
    echo "❌ ERROR: Falló la construcción de la imagen"
    echo "ℹ️  Revisa los logs anteriores para más detalles"
    exit 1
fi

echo ""
echo "🚀 INICIANDO CONTENEDOR EN MODO AUTOMÁTICO..."

# Iniciar en modo detached (background)
if $COMPOSE_CMD up -d; then
    echo "✅ Contenedor iniciado exitosamente"
else
    echo "❌ ERROR: Falló el inicio del contenedor"
    exit 1
fi

echo ""
echo "🎉 === BITCOIN PRICE MONITOR CONFIGURADO Y EJECUTÁNDOSE ==="
echo "============================================================"
echo ""
echo "📊 ESTADO DEL SISTEMA:"
$COMPOSE_CMD ps
echo ""
echo "📋 INFORMACIÓN IMPORTANTE:"
echo "  • ✅ El sistema está ejecutándose 24/7 automáticamente"
echo "  • ⏰ Enviará reportes DIARIOS a las 9:00 AM (Argentina)"
echo "  • 🔄 Se reinicia automáticamente si hay problemas"
echo "  • 📧 No requiere intervención manual"
echo ""
echo "🔧 COMANDOS ÚTILES:"
echo "  Ver logs en tiempo real:"
echo "    $COMPOSE_CMD logs -f"
echo ""
echo "  Ver estado:"
echo "    $COMPOSE_CMD ps"
echo ""
echo "  Reiniciar:"
echo "    $COMPOSE_CMD restart"
echo ""
echo "  Detener:"
echo "    $COMPOSE_CMD down"
echo ""
echo "  Ver logs específicos:"
echo "    $COMPOSE_CMD logs bitcoin-monitor"
echo ""

# Mostrar logs iniciales
echo "📄 LOGS INICIALES (últimas 20 líneas):"
echo "----------------------------------------"
$COMPOSE_CMD logs --tail=20 bitcoin-monitor

echo ""
echo "🎯 ¡CONFIGURACIÓN COMPLETADA!"
echo "El sistema ahora funciona completamente automático."
echo "Los reportes se enviarán diariamente a las 9:00 AM sin intervención manual."
