# Se añade 'json'
from flask import Flask, jsonify, render_template_string, request, redirect, url_for
import json

app = Flask(__name__)

# --- NUEVA FUNCIÓN ---
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

# Lista ahora se inicializa con los datos del JSON
dispositivos_registrados = cargar_datos_iniciales()
# --- FIN NUEVA FUNCIÓN ---

@app.route('/formulario')
def formulario():
    return render_template_string("""
    <html>
    <head><title>Agregar Dispositivo</title></head>
    <body>
        <h1>Nuevo Dispositivo</h1>
       <form action="/agregar" method="GET">
            SID: <input type="text" name="sid"><br>
            Nombre: <input type="text" name="nombre"><br>
            IP: <input type="text" name="ip"><br>
            Protocolos (separados por coma): <input type="text" name="protocolos"><br>
            Observaciones: <input type="text" name="observaciones"><br>
            <input type="submit" value="Registrar dispositivo">
        </form>
    </body>
    </html>
    """)

@app.route('/agregar', methods=['GET'])
def agregar_dispositivo():
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
    html = ""
    for d in dispositivos_registrados:
        html += f"""
        <div style="border:1px solid #ccc; padding:10px; margin:10px;">
            <strong>{d['sid']}</strong><br>
            <b>Nombre:</b> {d['nombre']}<br>
            <b>IP:</b> {d['ip']}<br>
            <b>Protocolos:</b> {', '.join(d['protocolos'])}<br>
            <b>Observaciones:</b> {d['observaciones']}
        </div>
        """

    return render_template_string(f"""
    <html>
    <head><title>Dispositivos de Red</title></head>
    <body>
        <h1>Lista de Dispositivos</h1>
        <a href="/formulario">Agregar nuevo dispositivo</a>
        {html}
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True)