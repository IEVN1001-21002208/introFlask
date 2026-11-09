from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

def obtener_conexion():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='',
        db='pizzeria_db',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"mensaje": "Sistema de Pizzería Activo"})

@app.route('/api/pedidos', methods=['GET'])
def get_pedidos():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM pedidos ORDER BY id DESC")
            pedidos = cursor.fetchall()
        conexion.close()
        return jsonify(pedidos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/pedidos', methods=['POST'])
def crear_pedido():
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql_pedido = "INSERT INTO pedidos (nombre_cliente, direccion, telefono, fecha_pedido, total_pedido) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_pedido, (data['nombre_cliente'], data['direccion'], data['telefono'], data['fecha_pedido'], data['total_pedido']))
            pedido_id = cursor.lastrowid
            
            sql_detalle = "INSERT INTO detalle_pedidos (pedido_id, tamano, ingredientes, num_pizzas, subtotal) VALUES (%s, %s, %s, %s, %s)"
            for item in data.get('detalles', []):
                cursor.execute(sql_detalle, (pedido_id, item['tamano'], ", ".join(item['ingredientes']), item['num_pizzas'], item['subtotal']))
            conexion.commit()
        conexion.close()
        return jsonify({"mensaje": "Pedido registrado", "id": pedido_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/pedidos/<int:id>', methods=['PUT'])
def actualizar_pedido(id):
    try:
        data = request.get_json()
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql_update = "UPDATE pedidos SET nombre_cliente=%s, direccion=%s, telefono=%s, fecha_pedido=%s, total_pedido=%s WHERE id=%s"
            cursor.execute(sql_update, (data['nombre_cliente'], data['direccion'], data['telefono'], data['fecha_pedido'], data['total_pedido'], id))
            
            cursor.execute("DELETE FROM detalle_pedidos WHERE pedido_id = %s", (id,))
            sql_detalle = "INSERT INTO detalle_pedidos (pedido_id, tamano, ingredientes, num_pizzas, subtotal) VALUES (%s, %s, %s, %s, %s)"
            for item in data.get('detalles', []):
                cursor.execute(sql_detalle, (id, item['tamano'], ", ".join(item['ingredientes']), item['num_pizzas'], item['subtotal']))
            
            conexion.commit()
        conexion.close()
        return jsonify({"mensaje": "Pedido actualizado"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/pedidos/<int:id>', methods=['DELETE'])
def eliminar_pedido(id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM pedidos WHERE id = %s", (id,))
            conexion.commit()
        conexion.close()
        return jsonify({"mensaje": "Pedido eliminado correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ventas/dia/<dia>', methods=['GET'])
def ventas_por_dia(dia):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SET lc_time_names = 'es_ES';") 
            cursor.execute("SELECT * FROM pedidos WHERE DAYNAME(fecha_pedido) = %s", (dia,))
            ventas = cursor.fetchall()
        conexion.close()
        return jsonify(ventas)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ventas/mes/<mes>', methods=['GET'])
def ventas_por_mes(mes):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SET lc_time_names = 'es_ES';")
            cursor.execute("SELECT * FROM pedidos WHERE MONTHNAME(fecha_pedido) = %s", (mes,))
            ventas = cursor.fetchall()
        conexion.close()
        return jsonify(ventas)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)