import threading
import time
import pymysql
from plyer import notification  
import pygame
import os
from flask import Blueprint, jsonify
from config import DB_CONFIG 

# Rutas de archivos
SONIDO_ALERTA = "./static/alerta/public_alerta.mp3"
ICONO_PATH = "./static/alerta/imagen_prueba.png"

alerta_blueprint = Blueprint('alerta', __name__)

pygame.mixer.init()
notificaciones_enviadas = set()
alerta_thread = None
is_alerting = False

def obtener_ultimo_numero():
    with pymysql.connect(**DB_CONFIG) as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT MAX(numero) as max_numero FROM reporte")
            resultado = cursor.fetchone()
            return resultado['max_numero'] if resultado['max_numero'] is not None else 0

def verificar_nuevos_registros(ultimo_numero_conocido):
    with pymysql.connect(**DB_CONFIG) as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM reporte WHERE numero > %s", (ultimo_numero_conocido,))
            return cursor.fetchall()

def reproducir_sonido():
    if os.path.exists(SONIDO_ALERTA):
        pygame.mixer.music.load(SONIDO_ALERTA)
        pygame.mixer.music.play()
    else:
        print(f"Archivo de sonido no encontrado: {SONIDO_ALERTA}. Asegúrate de que la ruta sea correcta.")

def enviar_notificacion(registro):
    global notificaciones_enviadas

    if registro['numero'] not in notificaciones_enviadas:
        reproducir_sonido()

        # Cambia la implementación de notificaciones aquí
        notification.notify(
            title=f"Nuevo reporte en: {registro['zona']}",
            message=f"Hora: {registro['hora']}\nAtaque: {registro['ataco']}\nObservaciones: {registro['observaciones']}",
            app_name='Sistema de Alerta',
            timeout=10,  # Duración de la notificación en segundos
        )

        notificaciones_enviadas.add(registro['numero'])

def alerta():
    global is_alerting
    ultimo_numero_conocido = obtener_ultimo_numero()
    print("Sistema de alerta activado...")

    while is_alerting:
        nuevos_registros = verificar_nuevos_registros(ultimo_numero_conocido)
        for registro in nuevos_registros:
            enviar_notificacion(registro)
            ultimo_numero_conocido = registro['numero']
        
        time.sleep(3)

def init_alerta():
    global alerta_thread, is_alerting
    is_alerting = True
    alerta_thread = threading.Thread(target=alerta)
    alerta_thread.start()
