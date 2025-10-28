# Se cambia render_template_string por render_template
from flask import Flask, jsonify, render_template, request, redirect, url_for
import json

# __name__ es necesario para que Flask encuentre la carpeta 'templates'
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

@app.route('/formulario')
def formulario():
    # MODIFICADO: Ahora usa el archivo de plantilla
    return render_template('formulario.html')

@app.route('/agregar', methods=['GET'])
def agregar_dispositivo():
    # (La lógica aquí no cambia)
    data = {
        "sid": request.args.get('sid'),
        "nombre": request.args.get('nombre'),
        "ip": request.args.get('ip'),
        "protocolos": [p.strip() for p in request.args.get('protocolos', '').split(',')],
        "observaciones": request.args.get('observaciones')
    }
    dispositivos_registrados.append(data)
    return redirect(url_for('mostrar_dispositivos'))

@app.route('/dispositivos')
def mostrar_dispositivos():
    # MODIFICADO: Pasa la variable a la plantilla
    return render_template('dispositivos.html', dispositivos=dispositivos_registrados)

if __name__ == '__main__':
    app.run(debug=True)