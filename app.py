# INSTALACIÓN DE FLASK:
# 1. cd C:/Users/TuUsuario/Documents/Flask_
# 2. python -m venv venv
# 3. venv\Scripts\activate
# 4. pip install flask
# 5. pip show flask
# 6. python app.py

# ... (Imports y funciones auxiliares sin cambios) ...
from flask import Flask, jsonify, render_template, request, redirect, url_for, abort
import json

app = Flask(__name__) 
def cargar_datos_iniciales():
    # ...
    return []
dispositivos_registrados = cargar_datos_iniciales()
def _find_device(sid):
    return next((d for d in dispositivos_registrados if d['sid'] == sid), None)

# --- RUTAS WEB (HTML) ---
# ... (Toda la sección WEB sin cambios) ...
@app.route('/')
# ...
@app.route('/vista/formulario')
# ...
@app.route('/vista/agregar', methods=['POST'])
# ...
@app.route('/vista/dispositivos')
# ...
@app.route('/vista/eliminar/<string:sid>', methods=['POST'])
# ...
@app.route('/vista/editar/<string:sid>')
# ...
@app.route('/vista/actualizar/<string:sid>', methods=['POST'])
# ...

# --- RUTAS API (JSON PARA POSTMAN) ---
# (Esta sección ha sido reescrita para incluir CRUD completo)

@app.route('/api/dispositivos', methods=['GET'])
def api_get_dispositivos():
    """(API GET) Obtiene todos los dispositivos."""
    return jsonify(dispositivos_registrados)

@app.route('/api/dispositivos', methods=['POST'])
def api_add_dispositivo():
    """(API POST) Agrega un nuevo dispositivo."""
    if not request.json:
        return jsonify({"error": "La solicitud debe ser de tipo JSON"}), 400
    data = request.json
    if not data.get('sid') or not data.get('nombre'):
        return jsonify({"error": "Los campos 'sid' y 'nombre' son obligatorios"}), 400
    
    if _find_device(data.get('sid')):
         return jsonify({"error": "Ya existe un dispositivo con ese SID"}), 400

    nuevo_dispositivo = {
        "sid": data.get('sid'),
        "nombre": data.get('nombre'),
        "ip": data.get('ip', 'N/A'),
        "protocolos": data.get('protocolos', []),
        "observaciones": data.get('observaciones', '')
    }
    dispositivos_registrados.append(nuevo_dispositivo)
    return jsonify(nuevo_dispositivo), 201

@app.route('/api/dispositivos/<string:sid>', methods=['GET'])
def api_get_dispositivo_por_id(sid):
    """(API GET por ID) Obtiene un dispositivo específico."""
    device = _find_device(sid)
    if not device:
        return jsonify({"error": "Dispositivo no encontrado"}), 404
    return jsonify(device)

@app.route('/api/dispositivos/<string:sid>', methods=['PUT'])
def api_update_dispositivo(sid):
    """(API PUT) Actualiza un dispositivo existente."""
    device = _find_device(sid)
    if not device:
        return jsonify({"error": "Dispositivo no encontrado"}), 404
    
    if not request.json:
        return jsonify({"error": "La solicitud debe ser de tipo JSON"}), 400
    
    data = request.json
    
    # Actualizamos el dispositivo
    device['nombre'] = data.get('nombre', device['nombre'])
    device['ip'] = data.get('ip', device['ip'])
    device['protocolos'] = data.get('protocolos', device['protocolos'])
    device['observaciones'] = data.get('observaciones', device['observaciones'])
    
    return jsonify(device)

@app.route('/api/dispositivos/<string:sid>', methods=['DELETE'])
def api_delete_dispositivo(sid):
    """(API DELETE) Elimina un dispositivo."""
    global dispositivos_registrados
    device = _find_device(sid)
    if not device:
        return jsonify({"error": "Dispositivo no encontrado"}), 404
    
    # Eliminamos el dispositivo
    dispositivos_registrados = [d for d in dispositivos_registrados if d['sid'] != sid]
    
    # Devolvemos una respuesta vacía con código 204 (No Content)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)