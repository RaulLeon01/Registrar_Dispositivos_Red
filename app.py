# INSTALACIÓN DE FLASK:
# 1. cd C:/Users/TuUsuario/Documents/Flask_
# 2. python -m venv venv
# 3. venv\Scripts\activate
# 4. pip install flask
# 5. pip show flask
# 6. python app.py

from flask import Flask, jsonify, render_template, request, redirect, url_for, abort
import json

app = Flask(__name__) 

def cargar_datos_iniciales():
    """Carga los dispositivos desde un archivo JSON."""
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Advertencia: No se encontró data.json, iniciando con lista vacía.")
        return []
    except json.JSONDecodeError:
        print("Error: data.json no es un JSON válido, iniciando con lista vacía.")
        return []

# Variable global para almacenar los datos
dispositivos_registrados = cargar_datos_iniciales()

def _find_device(sid):
    """Encuentra un dispositivo por su SID."""
    return next((d for d in dispositivos_registrados if d['sid'] == sid), None)

# --- RUTAS WEB (HTML) ---

@app.route('/')
def index():
    """Ruta raíz, redirige a la lista de dispositivos web."""
    return redirect(url_for('mostrar_dispositivos_web'))

@app.route('/vista/resetear', methods=['POST'])
def resetear_datos_web():
    """Recarga los datos desde data.json, reseteando la lista."""
    global dispositivos_registrados
    dispositivos_registrados = cargar_datos_iniciales()
    return redirect(url_for('mostrar_dispositivos_web'))

@app.route('/vista/formulario')
def formulario_web():
    """Muestra el formulario para agregar un nuevo dispositivo."""
    return render_template('formulario.html')

@app.route('/vista/agregar', methods=['POST'])
def agregar_dispositivo_web():
    """Ruta que procesa el formulario HTML para agregar."""
    data = {
        "sid": request.form.get('sid'),
        "nombre": request.form.get('nombre'),
        "ip": request.form.get('ip'),
        "protocolos": [p.strip() for p in request.form.get('protocolos', '').split(',')],
        "observaciones": request.form.get('observaciones')
    }
    dispositivos_registrados.append(data)
    return redirect(url_for('mostrar_dispositivos_web'))

@app.route('/vista/dispositivos')
def mostrar_dispositivos_web():
    """Muestra la lista de dispositivos en HTML."""
    return render_template('dispositivos.html', dispositivos=dispositivos_registrados)

@app.route('/vista/eliminar/<string:sid>', methods=['POST'])
def eliminar_dispositivo_web(sid):
    """Ruta que elimina un dispositivo (desde el formulario web)."""
    global dispositivos_registrados
    dispositivos_registrados = [d for d in dispositivos_registrados if d['sid'] != sid]
    return redirect(url_for('mostrar_dispositivos_web'))

@app.route('/vista/editar/<string:sid>')
def editar_dispositivo_web(sid):
    """Muestra el formulario de edición para un dispositivo."""
    device = _find_device(sid)
    if not device:
        abort(404)
    return render_template('editar.html', device=device)

@app.route('/vista/actualizar/<string:sid>', methods=['POST'])
def actualizar_dispositivo_web(sid):
    """Procesa la actualización de un dispositivo existente (desde el formulario web)."""
    device = _find_device(sid)
    if not device:
        abort(404)
    
    # Actualizamos el diccionario del dispositivo
    device['nombre'] = request.form.get('nombre')
    device['ip'] = request.form.get('ip')
    device['protocolos'] = [p.strip() for p in request.form.get('protocolos', '').split(',')]
    device['observaciones'] = request.form.get('observaciones')
    
    return redirect(url_for('mostrar_dispositivos_web'))


# --- RUTAS API (JSON PARA POSTMAN) ---

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

# Esta línea debe estar en el margen izquierdo (sin indentación)
if __name__ == '__main__':
    app.run(debug=True)