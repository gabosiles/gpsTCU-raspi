import csv
import time
import sys
import os

# Cambiar directorio de imports para agregar apiManager
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '..', '..'))
sys.path.insert(0, project_root)

from src import apiManager

datos_path = 'tests/map/datos_gps.csv'


def send_gps_data():
    """Función para probar el envío de datos GPS a los clientes conectados.
    Esta función simula el envío de datos GPS desde un archivo CSV.
    """
    with open(datos_path, 'r') as csvfile:
        content = csv.reader(csvfile)

        for row in content:
            lat = float(row[0])
            lon = float(row[1])
            data = {
                "latitude": lat,
                "longitude": lon,
            }
            apiManager.put_data('location.json', data)
            time.sleep(apiManager.get_period())


if __name__ == "__main__":
    send_gps_data()
