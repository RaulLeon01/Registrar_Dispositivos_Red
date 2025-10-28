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
# ... (Rutas /, /vista/formulario, /vista/agregar, /vista/dispositivos, /vista/eliminar sin cambios) ...
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
def editar_dispositivo_web(sid):
    device = _find_device(sid)
    if not device:
        abort(404)
    return render_template('editar.html', device=device)

# --- NUEVA RUTA ---
@app.route('/vista/actualizar/<string:sid>', methods=['POST'])
def actualizar_dispositivo_web(sid):
    """Procesa la actualización de un dispositivo existente."""
    device = _find_device(sid)
    if not device:
        # Si no se encuentra, algo salió mal
        abort(404)
    
    # Actualizamos el diccionario del dispositivo
    device['nombre'] = request.form.get('nombre')
    device['ip'] = request.form.get('ip')
    device['protocolos'] = [p.strip() for p in request.form.get('protocolos', '').split(',')]
    device['observaciones'] = request.form.get('observaciones')
    
    # Redirigimos de vuelta a la lista
    return redirect(url_for('mostrar_dispositivos_web'))

# --- RUTAS API (JSON PARA POSTMAN) ---
# ... (Sin cambios en esta sección por ahora) ...

@app.route('/api/dispositivos', methods=['GET'])
# ...
@app.route('/api/dispositivos', methods=['POST'])
# ...

if __name__ == '__main__':
    app.run(debug=True)