from flask import Blueprint, jsonify, request, redirect, url_for, render_template



inicio_blueprint = Blueprint('inicio', __name__)

@inicio_blueprint.route("/")
def inicio():
    return render_template("inicio.html")

def init_app(app):
    app.register_blueprint(inicio_blueprint)

