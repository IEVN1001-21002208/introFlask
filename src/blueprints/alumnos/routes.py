from flask import Blueprint, jsonify, request
from database import mysql

alumnos_bp = Blueprint('alumnos', __name__, url_prefix='/alumnos')

def leer_alumno_bd(matricula):
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM alumnos WHERE matricula = %s"
        cursor.execute(sql, (matricula,))
        datos = cursor.fetchone()
        
        if datos != None:
            alumno = {
                "matricula": datos[0], 
                "nombre": datos[1],
                "apaterno": datos[2],
                "amaterno": datos[3],
                "correo": datos[4] 
            }
            return alumno
        else:
            return None
    except Exception as ex:
        raise ex 

@alumnos_bp.route("", methods=['GET'])
def lista_alumno():
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM alumnos"
        cursor.execute(sql)
        datos = cursor.fetchall()
        
        alumnos = []
        for fila in datos:
            alumno = {
                "matricula": fila[0],
                "nombre": fila[1], 
                "apaterno": fila[2], 
                "amaterno": fila[3], 
                "correo": fila[4]
            }
            alumnos.append(alumno)
            
        return jsonify({'alumnos': alumnos, 'mensaje': 'Lista de alumnos', 'exito': True})
        
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

@alumnos_bp.route("/<mat>", methods=['GET'])
def leer_alumnos(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno != None:
            return jsonify({'alumno': alumno, 'mensaje': "Alumno encontrado", 'exito': True})
        else:
            return jsonify({'alumno': alumno, 'mensaje': 'Alumno no encontrado', 'exito': False})
            
    except Exception as ex:
        return jsonify({"mensaje": f"Error: {str(ex)}", "exito": False})

@alumnos_bp.route("", methods=['POST'])
def registrar_alumno():
    try:
        alumno = leer_alumno_bd(request.json['matricula'])
        if alumno != None:
            return jsonify({'mensaje': 'Alumno ya existe, no se puede duplicar', 'exito': False})
        else:
            cursor = mysql.connection.cursor()
            
            sql = """INSERT INTO alumnos (matricula, nombre, apaterno, amaterno, correo) 
                     VALUES (%s, %s, %s, %s, %s)"""
            
            cursor.execute(sql, (
                request.json['matricula'],
                request.json['nombre'],
                request.json['apaterno'],
                request.json['amaterno'],
                request.json['correo']
            ))
            mysql.connection.commit()
            
            return jsonify({'mensaje': 'Alumno registrado correctamente', 'exito': True})
            
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})
    
@alumnos_bp.route('/<mat>', methods=['PUT'])
def actualizar_alumno(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno != None:
            cursor = mysql.connection.cursor()
            sql = """UPDATE alumnos SET nombre = %s,
                     apaterno = %s, amaterno = %s, correo = %s
                     WHERE matricula = %s"""
            
            cursor.execute(sql, (
                request.json['nombre'],
                request.json['apaterno'],
                request.json['amaterno'],
                request.json['correo'],
                mat
            ))
            mysql.connection.commit()
            
            return jsonify({'mensaje': "Alumno actualizado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Alumno no encontrado.", 'exito': False})
            
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

@alumnos_bp.route('/<mat>', methods=['DELETE'])
def eliminar_alumno(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno != None:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM alumnos WHERE matricula = %s"
            
            cursor.execute(sql, (mat,))
            mysql.connection.commit()
            
            return jsonify({'mensaje': "Alumno eliminado correctamente.", 'exito': True})
        else:
            return jsonify({'mensaje': "Alumno no encontrado.", 'exito': False})
            
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})