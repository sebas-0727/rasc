# diagrama.py

from flask import Blueprint, jsonify, render_template
import pymysql
from config import DB_CONFIG

diagrama_blueprint = Blueprint('diagrama', __name__)

def conectar():
    return pymysql.connect(**DB_CONFIG)

def datos_conteo():
    conn = None
    try:
        conn = conectar()
        cur = conn.cursor()
        consulta = """
        SELECT zona, COUNT(*) AS conteo
        FROM reporte
        GROUP BY zona
        """
        cur.execute(consulta)
        datos = cur.fetchall()
        return [list(row) for row in datos]  # Convert tuples to lists
    finally:
        if conn:
            conn.close()

@diagrama_blueprint.route("/diagrama")
def inicio():
    return render_template('diagrama.html')

@diagrama_blueprint.route('/datos')
def datos_json():
    datos = datos_conteo()
    return jsonify(datos)
