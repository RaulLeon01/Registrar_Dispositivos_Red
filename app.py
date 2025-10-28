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
@app.route('/')
def index():
    return redirect(url_for('mostrar_dispositivos_web'))

# --- NUEVA RUTA ---
@app.route('/vista/resetear', methods=['POST'])
def resetear_datos_web():
    """Recarga los datos desde data.json, reseteando la lista."""
    global dispositivos_registrados
    dispositivos_registrados = cargar_datos_iniciales()
    return redirect(url_for('mostrar_dispositivos_web'))

@app.route('/vista/formulario')
def formulario_web():
    # ...
    return render_template('formulario.html')

@app.route('/vista/agregar', methods=['POST'])
def agregar_dispositivo_web():
    # ...
    return redirect(url_for('mostrar_dispositivos_web'))

@app.route('/vista/dispositivos')
def mostrar_dispositivos_web():
    # ...
    return render_template('dispositivos.html', dispositivos=dispositivos_registrados)

@app.route('/vista/eliminar/<string:sid>', methods=['POST'])
def eliminar_dispositivo_web(sid):
    # ...
    return redirect(url_for('mostrar_dispositivos_web'))

@app.route('/vista/editar/<string:sid>')
def editar_dispositivo_web(sid):
    # ...
    return render_template('editar.html', device=device)

@app.route('/vista/actualizar/<string:sid>', methods=['POST'])
def actualizar_dispositivo_web(sid):
    # ...
    return redirect(url_for('mostrar_dispositivos_web'))


# --- RUTAS API (JSON PARA POSTMAN) ---
# ... (Toda la sección API sin cambios) ...
@app.route('/api/dispositivos', methods=['GET'])
# ...
@app.route('/api/dispositivos', methods=['POST'])
# ...
@app.route('/api/dispositivos/<string:sid>', methods=['GET'])
# ...
@app.route('/api/dispositivos/<string:sid>', methods=['PUT'])
# ...
@app.route('/api/dispositivos/<string:sid>', methods=['DELETE'])
# ...

if __name__ == '__main__':
    app.run(debug=True)