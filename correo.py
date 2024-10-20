import smtplib
import os
import pymysql
import logging
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import DB_CONFIG
from flask import Blueprint
from threading import Thread

correo_blueprint = Blueprint('correo', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

def obtener_correos_activos():
    conexion = pymysql.connect(**DB_CONFIG)
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT correo FROM p_siga WHERE activo = 1")
            correos = cursor.fetchall()
            correos_lista = [correo[0] for correo in correos]
            logging.debug(f"Correos activos obtenidos: {correos_lista}")
            return correos_lista
    except Exception as e:
        logging.error(f"Error al obtener correos activos: {e}")
        return []
    finally:
        conexion.close()

def obtener_ultimo_numero_reporte():
    conexion = pymysql.connect(**DB_CONFIG)
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT numero FROM reporte ORDER BY numero DESC LIMIT 1")
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
    except Exception as e:
        logging.error(f"Error al obtener el último número de reporte: {e}")
        return None
    finally:
        conexion.close()

def enviar_correo_nuevo_reporte(numero_reporte):
    destinatarios = obtener_correos_activos()
    if not destinatarios:
        logging.warning("No se encontraron destinatarios activos.")
        return

    remitente = os.getenv('USER')
    password = os.getenv('PASS')
    
    if not remitente or not password:
        logging.error("Faltan credenciales de correo (USER o PASS).")
        return

    asunto = f'Nuevo reporte'
    msg = MIMEMultipart()
    msg['Subject'] = asunto
    msg['From'] = remitente
    msg['To'] = ', '.join(destinatarios)

    try:
        # Leer el contenido HTML directamente desde el archivo
        with open('correo.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        html_content = html_content.replace('{{numero_reporte}}', str(numero_reporte))
        msg.attach(MIMEText(html_content, 'html'))
    except Exception as e:
        logging.error(f"Error al cargar la plantilla de correo: {e}")
        return

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        
        texto = msg.as_string()
        server.sendmail(remitente, destinatarios, texto)
        logging.info(f"Correo enviado exitosamente a {len(destinatarios)} destinatarios.")
    except Exception as e:
        logging.error(f"Error al enviar el correo: {e}")
    finally:
        server.quit()

def verificar_y_enviar_inmediatamente():
    ultimo_numero_guardado = obtener_ultimo_numero_reporte()
    while True:
        try:
            nuevo_numero = obtener_ultimo_numero_reporte()
            if nuevo_numero and nuevo_numero != ultimo_numero_guardado:
                logging.info(f"Nuevo reporte detectado: {nuevo_numero}")
                enviar_correo_nuevo_reporte(nuevo_numero)
                ultimo_numero_guardado = nuevo_numero
        except Exception as e:
            logging.error(f"Error en la verificación de nuevos reportes: {e}")

def init_correo():
    thread = Thread(target=verificar_y_enviar_inmediatamente)
    thread.daemon = True
    thread.start()
    logging.info("Iniciado el hilo de verificación y envío inmediato de nuevos reportes.")
