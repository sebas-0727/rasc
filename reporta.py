from flask import Blueprint, jsonify, request, redirect, url_for, render_template




reporta_blueprint = Blueprint('reporta',__name__)

@reporta_blueprint.route("/reporta")
def contact():
    return render_template("reporta.html")

def init_app(app):
    app.register_blueprint(reporta_blueprint)
