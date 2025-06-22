from flask import Flask, render_template
from flask_socketio import SocketIO
import time
from apiManager import get_data, get_period

app = Flask(__name__, template_folder='../resources/templates')
socketio = SocketIO(app, cors_allowed_origins="*")

period = get_period()


@app.route('/')
def index():
    """
    Ruta principal que renderiza la plantilla del mapa.

    :return: Plantilla HTML del mapa.
    :rtype: flask.Response
    """
    return render_template('map.html')


def send_gps_data():
    """
    Envía datos GPS a los clientes conectados a través de WebSocket.

    Esta función se ejecuta en segundo plano y realiza solicitudes
    periódicas a la API para obtener la ubicación actual, luego
    transmite los datos a todos los clientes conectados.
    """
    while True:
        # Realiza la solicitud HTTP a la API para obtener los datos GPS
        data = get_data('location.json')
        lat = data['latitude']
        lon = data['longitude']
        socketio.emit('gps_update', {'lat': lat, 'lon': lon})
        time.sleep(period)


@socketio.on('connect')
def handle_connect():
    """
    Maneja el evento de conexión de un cliente al servidor WebSocket.

    Imprime un mensaje en la consola indicando que un cliente se ha conectado.
    """
    print("Cliente conectado")


if __name__ == '__main__':
    socketio.start_background_task(send_gps_data)
    socketio.run(app, debug=True, host='0.0.0.0',
                 port=5000, allow_unsafe_werkzeug=True)
