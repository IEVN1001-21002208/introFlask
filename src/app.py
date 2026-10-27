from flask import Flask
from flask_cors import CORS

from config import config
from database import mysql

from blueprints import registrar_blueprints

app = Flask(__name__)

app.json.ensure_ascii = False

app.config.from_object(config['development'])

CORS(app)
mysql.init_app(app)

registrar_blueprints(app)

def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == "__main__":
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host='0.0.0.0', port=5000)