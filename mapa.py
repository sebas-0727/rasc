import json
from flask import Flask, Blueprint, jsonify, render_template
import pymysql
from config import DB_CONFIG  # Asegúrate de que config.py esté en el mismo directorio o ajusta la ruta según sea necesario

# Configuración del blueprint
mapa_blueprint = Blueprint('mapa', __name__)

@mapa_blueprint.route("/mapa")
def inicio():
    return render_template("mapa.html")

@mapa_blueprint.route("/contador")
def obtener_reportes():
    connection = None  # Inicializar connection en None
    try:
        # Establecer la conexión
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['db'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            # Consulta SQL
            sql = "SELECT zona, COUNT(*) AS cantidad_reportes FROM reporte GROUP BY zona"
            cursor.execute(sql)
            report_counts = cursor.fetchall()

            # Devolver los datos en formato JSON
            return jsonify(report_counts)

    except pymysql.MySQLError as e:
        print(f"Error de conexión a la base de datos: {e}")
        return jsonify({'error': 'No se pudo conectar a la base de datos.'}), 500

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return jsonify({'error': str(e)}), 500

    finally:
        if connection:
            connection.close()

def init_app(app):
    app.register_blueprint(mapa_blueprint)
