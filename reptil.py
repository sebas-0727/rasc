from flask import Blueprint, jsonify, request, redirect, url_for, render_template



reptil_blueprint = Blueprint('reptil', __name__)

@reptil_blueprint.route("/reptil")
def inicio():
    return render_template("reptil.html")

def init_app(app):
    app.register_blueprint(reptil_blueprint)

