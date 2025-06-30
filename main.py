import os
import sys
import time
import schedule
import logging
from datetime import datetime
import pytz
from bitcoin_scraper import BitcoinScraper
from email_sender import EmailSender
from dotenv import load_dotenv

# Detectar si estamos en Docker o Windows
if os.path.exists('/app'):
    LOG_DIR = '/app/logs'
else:
    LOG_DIR = './logs'

# Crear directorio de logs si no existe
os.makedirs(LOG_DIR, exist_ok=True)

# Configurar logging con encoding UTF-8 para Windows
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{LOG_DIR}/bitcoin_monitor.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def send_bitcoin_report():
    """Función principal que obtiene el precio y envía el email"""
    try:
        logger.info("=== INICIANDO REPORTE DIARIO DE BITCOIN ===")
        
        # Obtener datos de Bitcoin
        scraper = BitcoinScraper()
        bitcoin_data = scraper.get_bitcoin_price()
        scraper.close()
        
        if not bitcoin_data:
            logger.error("No se pudieron obtener los datos de Bitcoin")
            return False
        
        logger.info(f"Precio obtenido: {bitcoin_data['price']}")
        
        # Enviar email
        email_sender = EmailSender()
        result = email_sender.send_email(bitcoin_data)
        
        if result:
            logger.info("[OK] Reporte enviado exitosamente")
            return True
        else:
            logger.error("[ERROR] Error al enviar el reporte")
            return False
            
    except Exception as e:
        logger.error(f"Error en send_bitcoin_report: {e}")
        return False

def run_scheduler():
    """Ejecuta el programador que envía el reporte diariamente a las 9 AM"""
    load_dotenv()
    
    timezone = os.getenv('TIMEZONE', 'America/Argentina/Buenos_Aires')
    tz = pytz.timezone(timezone)
    
    # Programar para las 9:00 AM todos los días
    schedule.every().day.at("09:00").do(send_bitcoin_report)
    
    logger.info(f"[SCHEDULER] Programador iniciado - Enviara reportes diarios a las 9:00 AM ({timezone})")
    logger.info("[INFO] Presiona Ctrl+C para detener")
    
    # Ejecutar inmediatamente una vez para verificar que funciona
    logger.info("[TEST] Ejecutando prueba inicial...")
    send_bitcoin_report()
    
    # Mantener el programador corriendo
    while True:
        schedule.run_pending()
        time.sleep(60)  # Verificar cada minuto

def main():
    """Función principal"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "test":
            logger.info("[TEST] Modo de prueba - Ejecutando una vez")
            result = send_bitcoin_report()
            sys.exit(0 if result else 1)
            
        elif command == "schedule":
            logger.info("[SCHEDULE] Modo programado - Ejecutando diariamente")
            run_scheduler()
            
        else:
            print("Uso: python main.py [test|schedule]")
            print("  test     - Ejecutar una vez como prueba")
            print("  schedule - Ejecutar programado diariamente")
            sys.exit(1)
    else:
        # Por defecto, ejecutar el programador
        run_scheduler()

if __name__ == "__main__":
    main()
