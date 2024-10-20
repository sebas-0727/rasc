# avistador.py

from flask import Blueprint, jsonify, request, redirect, url_for, render_template
import pymysql
from config import DB_CONFIG


avistador_blueprint = Blueprint('avistador', __name__)

@avistador_blueprint.route("/avistador", methods=['GET'])
def avistador():
    return render_template("avistador.html")

@avistador_blueprint.route("/admin", methods=['GET'])
def admin():
    return render_template("admin.html")

def conectar():
    return pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        db=DB_CONFIG['db'], 
        port=DB_CONFIG.get('port', 3306)
    )
@avistador_blueprint.route("/registrar_avistador", methods=['POST'])
def registra_avistador():
    conn = conectar()
    cur = conn.cursor()
    
    check_sql = "SELECT id, conteo FROM avistador WHERE correo = %s"
    cur.execute(check_sql, (request.json['correo'],))
    result = cur.fetchone()
    
    if result:
        avistador_id, conteo = result
        update_sql = "UPDATE avistador SET conteo = %s WHERE id = %s"
        cur.execute(update_sql, (conteo + 1, avistador_id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('avistador.reporte'))
    else:
        sql = "INSERT INTO avistador (nombres, ficha, correo, conteo) VALUES (%s, %s, %s, 1)"
        cur.execute(sql, (request.json['nombres'], request.json['ficha'], request.json['correo']))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('avistador.reporte'))

@avistador_blueprint.route("/avistador_general", methods=['GET'])
def consulta_general():
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT id, nombres, ficha, correo, conteo FROM avistador")
        rows = cur.fetchall()
        data = [{'id': row[0], 'nombres': row[1], 'ficha': row[2], 'correo': row[3], 'conteo': row[4]} for row in rows]
        cur.close()
        conn.close()
        return jsonify({'avistadores': data, 'mensaje': 'Avistadores registrados'})
    
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error al consultar avistadores'}), 500

@avistador_blueprint.route("/eliminar_avistador/<int:id>", methods=['DELETE'])
def eliminar_avistador(id):
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM avistador WHERE id=%s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Avistador eliminado correctamente'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error al eliminar avistador'}), 500

@avistador_blueprint.route("/reporte", methods=['GET'])
def reporte():
    return render_template("reporte.html")
