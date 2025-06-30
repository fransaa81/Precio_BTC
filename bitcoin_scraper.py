import requests
import logging
from datetime import datetime
import pytz

def get_bitcoin_price():
    """
    Obtiene el precio actual de Bitcoin usando la API de CoinGecko
    Returns: tuple (precio_usd, precio_ars, timestamp)
    """
    try:
        # API de CoinGecko - gratuita y confiable
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin',
            'vs_currencies': 'usd,ars',
            'include_last_updated_at': 'true'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        precio_usd = data['bitcoin']['usd']
        precio_ars = data['bitcoin']['ars']
        
        # Timestamp en zona horaria de Argentina
        argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
        timestamp = datetime.now(argentina_tz)
        
        logging.info(f"Precio obtenido exitosamente: USD ${precio_usd:,.2f} | ARS ${precio_ars:,.2f}")
        
        return precio_usd, precio_ars, timestamp
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Error de conexión al obtener precio de Bitcoin: {e}")
        return None, None, None
    except KeyError as e:
        logging.error(f"Error en formato de respuesta de API: {e}")
        return None, None, None
    except Exception as e:
        logging.error(f"Error inesperado al obtener precio de Bitcoin: {e}")
        return None, None, None

def format_price_report(precio_usd, precio_ars, timestamp):
    """
    Formatea el reporte de precio para email
    """
    if not all([precio_usd, precio_ars, timestamp]):
        return "❌ Error: No se pudo obtener el precio de Bitcoin"
    
    fecha_hora = timestamp.strftime("%d/%m/%Y a las %H:%M:%S")
    
    report = f"""
🚀 REPORTE DIARIO DE BITCOIN 🚀

📅 Fecha: {fecha_hora} (Argentina)
💰 Precio en USD: ${precio_usd:,.2f}
🇦🇷 Precio en ARS: ${precio_ars:,.2f}

📊 Información actualizada desde CoinGecko API
⚡ Sistema automatizado con Docker

¡Ten un excelente día! 🌟
"""
    
    return report.strip()
