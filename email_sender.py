import smtplib
import ssl
import os
import logging
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class EmailSender:
    def __init__(self):
        load_dotenv()
        self.smtp_server = os.getenv('ZOHO_SMTP_SERVER', 'smtp.zoho.com')
        self.smtp_port = int(os.getenv('ZOHO_SMTP_PORT', 587))
        self.email = os.getenv('ZOHO_EMAIL')
        self.password = os.getenv('ZOHO_PASSWORD')
        self.recipients = [email.strip() for email in os.getenv('RECIPIENT_EMAILS', '').split(',')]
        
        if not self.email or not self.password:
            raise ValueError("Credenciales de email no configuradas en .env")
        
        if not self.recipients or self.recipients == ['']:
            raise ValueError("Emails de destino no configurados en .env")
    
    def create_plain_email(self, bitcoin_data):
        """Crea un email simple en texto plano con el precio de Bitcoin"""
        
        # Determinar el emoji del cambio
        if bitcoin_data['is_positive']:
            trend_emoji = "↗"
        elif bitcoin_data['is_positive'] is False:
            trend_emoji = "↘"
        else:
            trend_emoji = "→"
        
        plain_content = f"""Precio de Bitcoin - {datetime.now().strftime('%d/%m/%Y')}

Precio actual: {bitcoin_data['price']}
Cambio 24h: {bitcoin_data['change']} {trend_emoji}
Rango 24h: {bitcoin_data['range_24h']}

Datos obtenidos: {bitcoin_data['timestamp']}
Fuente: {bitcoin_data['source']}
"""
        
        return plain_content
    
    def send_email(self, bitcoin_data):
        """Envía el email con la información de Bitcoin"""
        try:
            # Crear el mensaje simple de texto plano
            msg = MIMEText(self.create_plain_email(bitcoin_data), 'plain', 'utf-8')
            msg['Subject'] = f"Bitcoin: {bitcoin_data['price']} - {datetime.now().strftime('%d/%m/%Y')}"
            msg['From'] = self.email
            msg['To'] = ', '.join(self.recipients)
            
            # Conectar y enviar
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                logger.info(f"Intentando login con email: {self.email}")
                server.login(self.email, self.password)
                
                # Enviar a todos los destinatarios
                for recipient in self.recipients:
                    server.send_message(msg, to_addrs=[recipient])
                    logger.info(f"Email enviado exitosamente a {recipient}")
            
            logger.info(f"Emails enviados exitosamente a {len(self.recipients)} destinatarios")
            return True
            
        except Exception as e:
            logger.error(f"Error al enviar email: {e}")
            return False

def main():
    """Función para probar el envío de emails"""
    # Datos de prueba
    test_data = {
        'price': '$107,494',
        'change': '0.6%',
        'is_positive': False,
        'range_24h': '$107,379 - $108,771',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'source': 'CoinGecko'
    }
    
    try:
        sender = EmailSender()
        result = sender.send_email(test_data)
        
        if result:
            print("✅ Email de prueba enviado exitosamente")
        else:
            print("❌ Error al enviar email de prueba")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
