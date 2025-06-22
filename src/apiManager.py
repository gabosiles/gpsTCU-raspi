import requests
import configparser

config = configparser.ConfigParser()
config.read('pipeline.cfg')
url_base = config['api']['url']
token = config['api']['token']
db_path = config['db']['path']
period = config['scheduler']['period']


def get_db():
    """ Retorna dirección del archivo base de datos.

    :return: Path al archivo base de datos.
    :rtype: str
    """
    return db_path


def get_period():
    """ Retorna periodo de actualización de datos.

    :return: Periodo en segundos para procesos de actualización de datos.
    :rtype: float
    """
    return float(period)


def call_api(extension: str, data: dict, method: str):
    """ Llama a la API de UCR para enviar o recibir datos.

    Esta función realiza una solicitud HTTP (GET, POST, PUT) a la API
    utilizando una URL base configurada en el archivo de configuración.
    Dependiendo del método proporcionado, se envían datos o se reciben
    datos de la API.

    :param extension: La extensión añadida a la URL base para URL completa.
    :type extension: str
    :param data: Los datos a enviar a la API en formato diccionario.
    :type data: dict
    :param method: El método HTTP a utilizar ('GET', 'POST', 'PUT').
    :type method: str
    :return: La respuesta de la API en formato JSON.
    :rtype: dict
    :raises Exception: Si ocurre un error al hacer la solicitud a la API.
    """
    try:
        url = f'{url_base}/{extension}'
        header = {
            'Content-Type': 'application/json'

            # Quitar cuando se implemente el token en la API.
            # 'Authorization': 'Bearer ${token}'
        }
        mensaje = ''
        if method == 'GET':
            response = requests.get(url, headers=header)
            mensaje = "recibir"

        elif method == 'POST':
            response = requests.post(url, headers=header, json=data)
            mensaje = "enviar"

        elif method == 'PUT':
            response = requests.put(url, headers=header, json=data)
            mensaje = "actualizar"

        if not (response.status_code >= 200 & response.status_code < 300):
            print(
                f"Error al {mensaje} los datos a la API."
                f"Código de estado: {response.status_code}")
        return response.json()
    except Exception as e:
        print(f'Error al {mensaje} datos de la API: {e}')
        return []


def get_data(extension: str):
    """ Obtiene datos de la API utilizando el método GET.

    Esta función es un wrapper para la función `call_api`,
    realiza una solicitud GET a la API.

    :param extension: La extensión que se añade a la URL base.
    :type extension: str
    :return: La respuesta de la API en formato JSON.
    :rtype: dict
    """
    return call_api(extension, {}, 'GET')


def post_data(extension: str, data: dict):
    """ Envía datos a la API utilizando el método POST.

    Esta función es un wrapper para la función `call_api`,
    realiza una solicitud POST a la API.

    :param extension: La extensión que se añade a la URL base.
    :type extension: str
    :param data: Los datos a enviar a la API.
    :type data: dict
    :return: La respuesta de la API en formato JSON.
    :rtype: dict
    """
    return call_api(extension, data, 'POST')


def put_data(extension: str, data: dict):
    """ Actualiza datos en la API utilizando el método PUT.

    Esta función es un wrapper para la función `call_api`,
    realiza una solicitud PUT a la API.

    :param extension: La extensión que se añade a la URL base.
    :type extension: str
    :param data: Los datos a enviar a la API.
    :type data: dict
    :return: La respuesta de la API en formato JSON.
    :rtype: dict
    """
    return call_api(extension, data, 'PUT')
