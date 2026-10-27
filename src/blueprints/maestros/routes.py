from flask import Blueprint, jsonify, request
from database import mysql

maestros_bp = Blueprint('maestros', __name__, url_prefix='/api/maestros')

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))

def leer_maestro_bd(idmaestro):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT idmaestro, nombre, apaterno, amaterno, correo FROM maestro WHERE idmaestro = %s"
        cursor.execute(sql, (idmaestro,))
        datos = cursor.fetchone()
        if datos is not None:
            return fila_a_diccionario(cursor, datos)
        return None
    except Exception as ex:
        raise ex
    finally:
        if cursor is not None:
            cursor.close()

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

@maestros_bp.route('/<int:id>', methods=['GET'])
def leer_maestro(id):
    try:
        maestro = leer_maestro_bd(id)
        if maestro is not None:
            return jsonify({'maestro': maestro, 'mensaje': "Maestro encontrado", 'exito': True}), 200
        else:
            return jsonify({'maestro': None, 'mensaje': 'Maestro no encontrado', 'exito': False}), 404
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False}), 500

@maestros_bp.route('', methods=['POST'])
def registrar_maestro():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = """INSERT INTO maestro (nombre, apaterno, amaterno, correo) 
                 VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, (
            request.json['nombre'],
            request.json['apaterno'],
            request.json['amaterno'],
            request.json['correo']
        ))
        mysql.connection.commit()
        return jsonify({'mensaje': 'Maestro registrado correctamente', 'exito': True}), 201
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()

@maestros_bp.route('/<int:id>', methods=['PUT'])
def actualizar_maestro(id):
    cursor = None
    try:
        maestro = leer_maestro_bd(id)
        if maestro is not None:
            cursor = mysql.connection.cursor()
            sql = """UPDATE maestro SET nombre = %s, apaterno = %s, amaterno = %s, correo = %s 
                     WHERE idmaestro = %s"""
            cursor.execute(sql, (
                request.json['nombre'],
                request.json['apaterno'],
                request.json['amaterno'],
                request.json['correo'],
                id
            ))
            mysql.connection.commit()
            return jsonify({'mensaje': 'Maestro actualizado correctamente', 'exito': True}), 200
        else:
            return jsonify({'mensaje': 'Maestro no encontrado', 'exito': False}), 404
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()

@maestros_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_maestro(id):
    cursor = None
    try:
        maestro = leer_maestro_bd(id)
        if maestro is not None:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM maestro WHERE idmaestro = %s"
            cursor.execute(sql, (id,))
            mysql.connection.commit()
            return jsonify({'mensaje': 'Maestro eliminado correctamente', 'exito': True}), 200
        else:
            return jsonify({'mensaje': 'Maestro no encontrado', 'exito': False}), 404
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()