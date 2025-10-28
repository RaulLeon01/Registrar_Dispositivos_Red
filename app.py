# INSTALACIÓN DE FLASK:
# 1. cd C:/Users/TuUsuario/Documents/Flask_
# 2. python -m venv venv
# 3. venv/Scripts/activate
# 4. pip install flask
# 5. pip show flask
# 6. python app.py

from flask import Flask, jsonify, render_template, request, redirect, url_for
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

dispositivos_registrados = cargar_datos_iniciales()

# --- RUTAS WEB (HTML) ---

@app.route('/')
def index():
    """Ruta raíz, redirige a la lista de dispositivos web."""
    return redirect(url_for('mostrar_dispositivos_web'))

@app.route('/vista/formulario')
def formulario_web():
    return render_template('formulario.html')

@app.route('/vista/agregar', methods=['POST']) # CAMBIADO a POST
def agregar_dispositivo_web():
    """Ruta que procesa el formulario HTML."""
    # CAMBIADO a request.form para datos de formulario POST 
    data = {
        "sid": request.form.get('sid'),
        "nombre": request.form.get('nombre'),
        "ip": request.form.get('ip'),
        "protocolos": [p.strip() for p in request.form.get('protocolos', '').split(',')],
        "observaciones": request.form.get('observaciones')
    }
    dispositivos_registrados.append(data)
    # Redirige a la lista web
    return redirect(url_for('mostrar_dispositivos_web'))

@app.route('/vista/dispositivos') # Ruta renombrada
def mostrar_dispositivos_web():
    return render_template('dispositivos.html', dispositivos=dispositivos_registrados)


# --- RUTAS API (JSON PARA POSTMAN) ---

@app.route('/api/dispositivos', methods=['GET'])
def api_get_dispositivos():
    """
    (PARA POSTMAN) Obtiene todos los dispositivos en formato JSON.
    """
    return jsonify(dispositivos_registrados)

@app.route('/api/dispositivos', methods=['POST'])
def api_add_dispositivo():
    """
    (PARA POSTMAN) Agrega un nuevo dispositivo.
    Espera recibir un cuerpo (body) en formato JSON.
    """
    # Para API, usamos request.json
    if not request.json:
        return jsonify({"error": "La solicitud debe ser de tipo JSON"}), 400

    data = request.json
    
    # Validación simple
    if not data.get('sid') or not data.get('nombre'):
        return jsonify({"error": "Los campos 'sid' y 'nombre' son obligatorios"}), 400
    
    # Aseguramos la estructura de datos
    nuevo_dispositivo = {
        "sid": data.get('sid'),
        "nombre": data.get('nombre'),
        "ip": data.get('ip', 'N/A'),
        "protocolos": data.get('protocolos', []),
        "observaciones": data.get('observaciones', '')
    }

    dispositivos_registrados.append(nuevo_dispositivo)
    
    # Devolvemos el objeto creado y un código 201 (Created)
    return jsonify(nuevo_dispositivo), 201


if __name__ == '__main__':
    app.run(debug=True)