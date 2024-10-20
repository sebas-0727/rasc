# reptiles.py

from flask import Blueprint, request, jsonify, render_template
from flask_cors import CORS
import pymysql
from pymysql.err import IntegrityError
import base64
from config import DB_CONFIG
from pymysql.cursors import DictCursor  # Importar DictCursor

# Definir el Blueprint para reptiles
reptiles_blueprint = Blueprint('reptiles', __name__)
CORS(reptiles_blueprint)

# Función para conectar a la base de datos
def conectar():
    return pymysql.connect(cursorclass=DictCursor, **DB_CONFIG)  # Usar DictCursor

# Ruta para servir la página HTML
@reptiles_blueprint.route("/reptiles", methods=['GET'])
def reptiles():
    return render_template("reptiles.html")

# Ruta para registrar un nuevo reptil
@reptiles_blueprint.route("/registro_reptil", methods=['POST'])
def registrar_reptil():
    data = request.get_json()
    nombre_cientifico = data.get('nombre_cientifico')
    nombre = data.get('nombre')
    veneno = data.get('veneno')
    imagen_base64 = data.get('imagen')  # Imagen en formato Base64

    if not all([nombre_cientifico, nombre, veneno]):
        return jsonify({'mensaje': 'Todos los campos son requeridos.'}), 400
    
    # Convertir Base64 a binario
    imagen_binario = None
    if imagen_base64:
        try:
            imagen_binario = base64.b64decode(imagen_base64)
        except Exception as e:
            print(f"Error al decodificar la imagen: {e}")
            return jsonify({'mensaje': 'Error al procesar la imagen.'}), 400
    
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                sql = "INSERT INTO reptiles (nombre_cientifico, nombre, veneno, imagen) VALUES (%s, %s, %s, %s)"
                cur.execute(sql, (nombre_cientifico, nombre, veneno, imagen_binario))
                conn.commit()
        return jsonify({'mensaje': 'Reptil agregado correctamente'}), 201
    except IntegrityError as e:
        print(f"Error de integridad: {e}")
        if 'Duplicate entry' in str(e):
            return jsonify({'mensaje': 'Nombre científico ya existe'}), 409
        else:
            return jsonify({'mensaje': 'Error al agregar el reptil'}), 500
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error al agregar el reptil'}), 500

# Ruta para consultar todos los reptiles
@reptiles_blueprint.route("/reptiles/lista", methods=['GET'])
def consultar_reptiles():
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                sql = "SELECT * FROM reptiles"
                cur.execute(sql)
                reptiles = cur.fetchall()
                
                # Convertir las imágenes a Base64
                for reptil in reptiles:
                    if reptil['imagen']:
                        reptil['imagen'] = base64.b64encode(reptil['imagen']).decode('utf-8')
        return jsonify(reptiles), 200
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error al consultar los reptiles'}), 500

# Ruta para consultar un reptil por nombre científico
@reptiles_blueprint.route("/reptiles/nombre/<string:nombre_cientifico>", methods=['GET'])
def consultar_reptil_por_nombre(nombre_cientifico):
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                sql = "SELECT * FROM reptiles WHERE nombre_cientifico = %s"
                cur.execute(sql, (nombre_cientifico,))
                reptil = cur.fetchone()
                
                # Convertir la imagen a Base64 si existe
                if reptil and reptil['imagen']:
                    reptil['imagen'] = base64.b64encode(reptil['imagen']).decode('utf-8')
        if reptil:
            return jsonify(reptil), 200
        else:
            return jsonify({'mensaje': 'Reptil no encontrado'}), 404
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error al consultar el reptil'}), 500

# Ruta para eliminar un reptil por nombre científico
@reptiles_blueprint.route("/reptiles/nombre/<string:nombre_cientifico>", methods=['DELETE'])
def eliminar_reptil_por_nombre(nombre_cientifico):
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                sql = "DELETE FROM reptiles WHERE nombre_cientifico = %s"
                cur.execute(sql, (nombre_cientifico,))
                conn.commit()
        if cur.rowcount > 0:
            return jsonify({'mensaje': 'Reptil eliminado correctamente'}), 200
        else:
            return jsonify({'mensaje': 'Reptil no encontrado'}), 404
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error al eliminar el reptil'}), 500
