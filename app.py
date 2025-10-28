# INSTALACIÓN DE FLASK:
# 1. cd C:/Users/TuUsuario/Documents/Flask_
# 2. python -m venv venv
# 3. venv\Scripts\activate
# 4. pip install flask
# 5. pip show flask
# 6. python app.py

# ... (Imports sin cambios) ...
from flask import Flask, jsonify, render_template, request, redirect, url_for, abort
import json

app = Flask(__name__) 

# ... (cargar_datos_iniciales sin cambios) ...
def cargar_datos_iniciales():
    # ...
    return []

dispositivos_registrados = cargar_datos_iniciales()

# --- NUEVA FUNCIÓN AUXILIAR ---
def _find_device(sid):
    """Encuentra un dispositivo por su SID."""
    return next((d for d in dispositivos_registrados if d['sid'] == sid), None)

# --- RUTAS WEB (HTML) ---
# ... (Rutas /, /vista/formulario, /vista/agregar sin cambios) ...

@app.route('/')
def index():
    return redirect(url_for('mostrar_dispositivos_web'))

@app.route('/vista/formulario')
def formulario_web():
    return render_template('formulario.html')

@app.route('/vista/agregar', methods=['POST'])
def agregar_dispositivo_web():
    # ...
    return redirect(url_for('mostrar_dispositivos_web'))

@app.route('/vista/dispositivos')
def mostrar_dispositivos_web():
    return render_template('dispositivos.html', dispositivos=dispositivos_registrados)

@app.route('/vista/eliminar/<string:sid>', methods=['POST'])
def eliminar_dispositivo_web(sid):
    global dispositivos_registrados
    dispositivos_registrados = [d for d in dispositivos_registrados if d['sid'] != sid]
    return redirect(url_for('mostrar_dispositivos_web'))

# --- NUEVA RUTA ---
@app.route('/vista/editar/<string:sid>')
def editar_dispositivo_web(sid):
    """Muestra el formulario de edición para un dispositivo."""
    device = _find_device(sid)
    if not device:
        # Si no se encuentra el dispositivo, devuelve un error 404
        abort(404)
    return render_template('editar.html', device=device)

# --- RUTAS API (JSON PARA POSTMAN) ---
# ... (Sin cambios en esta sección por ahora) ...

@app.route('/api/dispositivos', methods=['GET'])
# ...
def api_get_dispositivos():
    return jsonify(dispositivos_registrados)

@app.route('/api/dispositivos', methods=['POST'])
# ...
def api_add_dispositivo():
    # ...
    return jsonify(nuevo_dispositivo), 201

if __name__ == '__main__':
    app.run(debug=True)