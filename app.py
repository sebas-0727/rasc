from flask import Flask
from flask_cors import CORS
from anfibio import anfibio_blueprint
from avistador import avistador_blueprint
from contact import contact_blueprint
from diagrama import diagrama_blueprint
from inicio import inicio_blueprint
from mapa import mapa_blueprint
from reporta import reporta_blueprint
from reporte import reporte_blueprint
from reptil import reptil_blueprint
from reptiles import reptiles_blueprint
from siga import siga_blueprint
from inicio_siga import inicio_siga_blueprint
from alerta import alerta_blueprint, init_alerta
from correo import correo_blueprint, init_correo

app = Flask(__name__)
CORS(app)

app.register_blueprint(avistador_blueprint) 
app.register_blueprint(siga_blueprint)
app.register_blueprint(diagrama_blueprint)
app.register_blueprint(reptiles_blueprint)
app.register_blueprint(reporte_blueprint)
app.register_blueprint(inicio_blueprint)
app.register_blueprint(contact_blueprint)
app.register_blueprint(reporta_blueprint)
app.register_blueprint(mapa_blueprint)
app.register_blueprint(reptil_blueprint)
app.register_blueprint(anfibio_blueprint)
app.register_blueprint(inicio_siga_blueprint)
app.register_blueprint(alerta_blueprint)
app.register_blueprint(correo_blueprint, url_prefix='/correo')

if __name__ == '__main__':
    init_alerta()
    init_correo()  
    app.run()