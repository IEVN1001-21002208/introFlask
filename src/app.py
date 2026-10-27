from flask import Flask
from flask_cors import CORS

# Importamos la configuración y la instancia de la base de datos
from config import config
from database import mysql

# Importamos las rutas (Blueprints) de los alumnos y maestros
from blueprints.alumnos.routes import alumnos_bp
from blueprints.maestros.routes import maestros_bp

app = Flask(__name__)

# 1. Cargar la configuración ANTES de la base de datos
app.config.from_object(config['development'])

# 2. Inicializar CORS y la base de datos con la aplicación
CORS(app)
mysql.init_app(app)

# 3. Registrar todos los Blueprints (Rutas modulares)
app.register_blueprint(alumnos_bp)
app.register_blueprint(maestros_bp)

# 4. Manejador de errores
def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == "__main__":
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host='0.0.0.0', port=5000)