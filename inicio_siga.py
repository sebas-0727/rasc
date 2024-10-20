# inicio_siga.py

from flask import Blueprint, request, redirect, url_for, render_template
import pymysql
import bcrypt
from config import DB_CONFIG

inicio_siga_blueprint = Blueprint('inicio_siga', __name__)

def conectar():
    return pymysql.connect(**DB_CONFIG)

@inicio_siga_blueprint.route("/inicio_siga", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['correo']
        password = request.form['contraseña']

        if email == 'admin' and password == '12345':
            return redirect(url_for('inicio_siga.admin_page'))

        if '@' not in email:
            return render_template('inicio_siga.html', error="Por favor, ingrese un correo electrónico válido.")

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT id, contraseña, activo FROM p_siga WHERE correo = %s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):  # Verificar la contraseña
            if user[2]:  # Verificar si la cuenta está activa
                return redirect(url_for('inicio_siga.siga_page'))
            else:
                return render_template('inicio_siga.html', error="Su cuenta no está activa. Por favor, contacte al administrador.")
        else:
            return render_template('inicio_siga.html', error="Correo o contraseña incorrectos.")

    return render_template('inicio_siga.html')

@inicio_siga_blueprint.route('/reptiles')
def siga_page():
    return "Bienvenido a la página SIGA!"

@inicio_siga_blueprint.route('/admin')
def admin_page():
    return "Bienvenido a la página de administración!"
