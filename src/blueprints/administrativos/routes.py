from flask import Blueprint, jsonify, request
from database import mysql

administrativos_bp = Blueprint('administrativos', __name__, url_prefix='/api/administrativos')

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))

def leer_administrativo_bd(numempleado):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT numempleado, nombre, apellidos, telefono, correo, departamento FROM administrativos WHERE numempleado = %s"
        cursor.execute(sql, (numempleado,))
        datos = cursor.fetchone()
        if datos is not None:
            return fila_a_diccionario(cursor, datos)
        return None
    except Exception as ex:
        raise ex
    finally:
        if cursor is not None:
            cursor.close()

@administrativos_bp.route('', methods=['GET'])
def lista_administrativos():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT numempleado, nombre, apellidos, telefono, correo, departamento FROM administrativos")
        datos = cursor.fetchall()
        administrativos = [fila_a_diccionario(cursor, fila) for fila in datos]
        return jsonify({'administrativos': administrativos, 'mensaje': 'Lista de administrativos', 'exito': True}), 200
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()

@administrativos_bp.route('/<int:id>', methods=['GET'])
def leer_administrativo(id):
    try:
        administrativo = leer_administrativo_bd(id)
        if administrativo is not None:
            return jsonify({'administrativo': administrativo, 'mensaje': "Administrativo encontrado", 'exito': True}), 200
        else:
            return jsonify({'administrativo': None, 'mensaje': 'Administrativo no encontrado', 'exito': False}), 404
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False}), 500

@administrativos_bp.route('', methods=['POST'])
def registrar_administrativo():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = """INSERT INTO administrativos (nombre, apellidos, telefono, correo, departamento) 
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (
            request.json['nombre'],
            request.json['apellidos'],
            request.json['telefono'],
            request.json['correo'],
            request.json['departamento']
        ))
        mysql.connection.commit()
        return jsonify({'mensaje': 'Administrativo registrado correctamente', 'exito': True}), 201
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()

@administrativos_bp.route('/<int:id>', methods=['PUT'])
def actualizar_administrativo(id):
    cursor = None
    try:
        administrativo = leer_administrativo_bd(id)
        if administrativo is not None:
            cursor = mysql.connection.cursor()
            sql = """UPDATE administrativos SET nombre = %s, apellidos = %s, telefono = %s, correo = %s, departamento = %s 
                     WHERE numempleado = %s"""
            cursor.execute(sql, (
                request.json['nombre'],
                request.json['apellidos'],
                request.json['telefono'],
                request.json['correo'],
                request.json['departamento'],
                id
            ))
            mysql.connection.commit()
            return jsonify({'mensaje': 'Administrativo actualizado correctamente', 'exito': True}), 200
        else:
            return jsonify({'mensaje': 'Administrativo no encontrado', 'exito': False}), 404
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()

@administrativos_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_administrativo(id):
    cursor = None
    try:
        administrativo = leer_administrativo_bd(id)
        if administrativo is not None:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM administrativos WHERE numempleado = %s"
            cursor.execute(sql, (id,))
            mysql.connection.commit()
            return jsonify({'mensaje': 'Administrativo eliminado correctamente', 'exito': True}), 200
        else:
            return jsonify({'mensaje': 'Administrativo no encontrado', 'exito': False}), 404
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False}), 500
    finally:
        if cursor is not None:
            cursor.close()