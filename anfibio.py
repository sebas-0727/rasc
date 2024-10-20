from flask import Blueprint, jsonify, request, redirect, url_for, render_template



anfibio_blueprint = Blueprint('anfibio', __name__)

@anfibio_blueprint.route("/anfibio")
def inicio():
    return render_template("anfibio.html")

def init_app(app):
    app.register_blueprint(anfibio_blueprint)


