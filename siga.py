# siga.py

from flask import Blueprint, jsonify, request, render_template
import pymysql
from functools import wraps
import bcrypt
from config import DB_CONFIG

siga_blueprint = Blueprint('siga', __name__)

def conectar():
    return pymysql.connect(**DB_CONFIG)

def login_requerido(f):
    @wraps(f)
    def funcion_decorada(*args, **kwargs):
        if 'id_usuario' not in request.cookies:
            return jsonify({'mensaje': 'Acceso no autorizado'}), 401
        return f(*args, **kwargs)
    return funcion_decorada

def encriptar_contraseña(contraseña):
    return bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verificar_contraseña(contraseña, contraseña_encriptada):
    return bcrypt.checkpw(contraseña.encode('utf-8'), contraseña_encriptada.encode('utf-8'))

@siga_blueprint.route("/siga", methods=['GET'])
def siga():
    return render_template("siga.html")

@siga_blueprint.route("/admin", methods=['GET'])
def admin():
    return render_template("admin.html")

@siga_blueprint.route("/registrar_siga", methods=['POST'])
def registrar_siga():
    try:
        conn = conectar()
        cur = conn.cursor()
        
        consulta_verificacion = "SELECT id FROM p_siga WHERE correo = %s"
        cur.execute(consulta_verificacion, (request.json['correo'],))
        resultado = cur.fetchone()
        
        if resultado:
            cur.close()
            conn.close()
            return jsonify({'mensaje': 'El correo ya está registrado'}), 400
        else:
            contraseña_encriptada = encriptar_contraseña(request.json['contraseña'])
            sql = "INSERT INTO p_siga (nombre, correo, contraseña, funcion, u_asignado, activo) VALUES (%s, %s, %s, %s, %s, %s)"
            cur.execute(sql, (request.json['nombre'], request.json['correo'], contraseña_encriptada, request.json['funcion'], 
                    request.json['u_asignado'], 1)) 
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'mensaje': 'Registro exitoso'}), 200
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error al registrar usuario'}), 500

@siga_blueprint.route("/siga_general", methods=['GET'])
def consulta_general():
    try:
        conn = conectar()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT id, nombre, correo, contraseña, funcion, activo, u_asignado FROM p_siga")
        filas = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({'siga': filas, 'mensaje': 'Registros SIGA obtenidos'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error al consultar registros SIGA'}), 500

@siga_blueprint.route("/actualizar_activo/<int:id>", methods=['PATCH'])
def actualizar_activo(id):
    try:
        conn = conectar()
        cur = conn.cursor()
        datos = request.get_json()
        activo = datos.get('activo')
        cur.execute("UPDATE p_siga SET activo=%s WHERE id=%s", (activo, id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Estado de activo actualizado correctamente'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error al actualizar estado'}), 500

@siga_blueprint.route("/cambiar_contraseña", methods=['GET'])
def pagina_cambiar_contraseña():
    return render_template("cambiar_contraseña.html")

@siga_blueprint.route("/cambiar_contraseña", methods=['PATCH'])
def cambiar_contraseña():
    try:
        conn = conectar()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        
        datos = request.get_json()
        correo = datos.get('correo')
        nueva_contraseña = datos.get('nueva_contraseña')
        
        cur.execute("SELECT id, activo FROM p_siga WHERE correo=%s", (correo,))
        resultado = cur.fetchone()

        if not resultado:
            cur.close()
            conn.close()
            return jsonify({'mensaje': 'Correo no encontrado'}), 404

        if not resultado['activo']:
            cur.close()
            conn.close()
            return jsonify({'mensaje': 'La cuenta está inactiva'}), 403

        nueva_contraseña_encriptada = encriptar_contraseña(nueva_contraseña)
        cur.execute("UPDATE p_siga SET contraseña=%s WHERE correo=%s", (nueva_contraseña_encriptada, correo))
        conn.commit()
        
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Contraseña actualizada correctamente'})
    
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error al cambiar la contraseña'}), 500

@siga_blueprint.route("/reptiles", methods=['GET'])
def exito():
    return render_template("reptiles.html")

def inicializar_app(app):
    app.register_blueprint(siga_blueprint)
