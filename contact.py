from flask import Blueprint, jsonify, request, redirect, url_for, render_template



contact_blueprint = Blueprint('contact', __name__)

@contact_blueprint.route("/contact")
def contact():
    return render_template("contact.html")

def init_app(app):
    app.register_blueprint(contact_blueprint)


