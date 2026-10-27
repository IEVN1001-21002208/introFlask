from flask import Blueprint, jsonify
from database import mysql

maestros_bp = Blueprint('maestros', __name__, url_prefix='/api/maestros')

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))

@maestros_bp.route('', methods=['GET'])
def lista_maestros():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT idmaestro, nombre, apaterno, amaterno, correo FROM maestro")
        datos = cursor.fetchall()
        
        maestros = [fila_a_diccionario(cursor, fila) for fila in datos]

        return jsonify({'maestros': maestros, 'mensaje': 'Lista de maestros', 'exito': True}), 200
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()