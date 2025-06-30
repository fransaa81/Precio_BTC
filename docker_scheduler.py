import os
import time
import schedule
import logging
import signal
import sys
from datetime import datetime
import pytz
from main import send_bitcoin_report

# Configurar logging robusto para Docker
def setup_logging():
    log_format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler('/app/logs/docker_scheduler.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# Variable global para control del scheduler
running = True

def signal_handler(sig, frame):
    """Manejo de señales para shutdown graceful"""
    global running
    logger.info(f"🛑 Recibida señal {sig}. Cerrando gracefully...")
    running = False

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def run_bitcoin_report_safe():
    """Wrapper seguro para ejecutar el reporte con manejo robusto de errores"""
    try:
        logger.info("🚀 === INICIANDO EJECUCIÓN PROGRAMADA ===")
        start_time = datetime.now()
        
        result = send_bitcoin_report()
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        if result:
            logger.info(f"✅ ÉXITO: Reporte completado en {duration}")
        else:
            logger.error(f"❌ FALLO: Error en ejecución (duración: {duration})")
            
        return result
    except Exception as e:
        logger.error(f"💥 EXCEPCIÓN: {e}", exc_info=True)
        return False

def main():
    """Scheduler Docker 100% automatizado - Ejecuta diariamente a las 9 AM Argentina"""
    global running
    
    # Configurar timezone para Argentina
    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    
    logger.info("🐳 === BITCOIN MONITOR DOCKER SCHEDULER ===")
    logger.info("=" * 70)
    logger.info("🎯 MODO: 100% AUTOMATIZADO - Sin intervención manual requerida")
    logger.info("📅 PROGRAMACIÓN: DIARIO a las 9:00 AM (Argentina)")
    logger.info("🌐 TIMEZONE: America/Argentina/Buenos_Aires")
    logger.info("⏰ HORA ACTUAL: " + datetime.now(argentina_tz).strftime('%Y-%m-%d %H:%M:%S %Z'))
    logger.info("🔄 REINICIO: unless-stopped (se reinicia automáticamente)")
    logger.info("=" * 70)
    
    # Programar la tarea diaria
    schedule.every().day.at("09:00").do(run_bitcoin_report_safe)
    
    # Ejecutar prueba inicial
    logger.info("🧪 EJECUTANDO PRUEBA INICIAL DEL SISTEMA...")
    try:
        initial_result = run_bitcoin_report_safe()
        if initial_result:
            logger.info("✅ PRUEBA INICIAL EXITOSA - Sistema funcionando correctamente")
            logger.info("📧 Los reportes se enviarán automáticamente cada día a las 9:00 AM")
        else:
            logger.error("❌ PRUEBA INICIAL FALLÓ - Verificar configuración")
    except Exception as e:
        logger.error(f"💥 ERROR EN PRUEBA INICIAL: {e}")
    
    logger.info("🔄 INICIANDO LOOP PRINCIPAL...")
    logger.info("ℹ️  Para monitorear: docker-compose logs -f")
    logger.info("ℹ️  Para detener: docker-compose down")
    
    # Loop principal - mantiene el contenedor vivo 24/7
    heartbeat_counter = 0
    while running:
        try:
            schedule.run_pending()
            time.sleep(60)  # Verificar cada minuto
            
            heartbeat_counter += 1
            
            # Log de estado cada hora (60 minutos)
            if heartbeat_counter >= 60:
                current_time = datetime.now(argentina_tz)
                next_run = schedule.next_run()
                if next_run:
                    next_run_local = next_run.astimezone(argentina_tz)
                    logger.info(f"💓 ESTADO: Sistema activo - Próxima ejecución: {next_run_local.strftime('%Y-%m-%d %H:%M:%S %Z')}")
                else:
                    logger.info("💓 ESTADO: Sistema activo - Esperando programación")
                heartbeat_counter = 0
                
        except KeyboardInterrupt:
            logger.info("🛑 SHUTDOWN: Solicitado por usuario (Ctrl+C)")
            break
        except Exception as e:
            logger.error(f"❌ ERROR EN SCHEDULER: {e}")
            logger.info("⏳ Esperando 5 minutos antes de continuar...")
            time.sleep(300)  # Esperar 5 minutos en caso de error
    
    logger.info("🏁 SCHEDULER FINALIZADO")

if __name__ == "__main__":
    main()
