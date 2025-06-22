import tkinter as tk
import threading
from funcionesGPS import manejarGPS
import sqlite3
from apiManager import get_db, post_data

# Dirección de la base de datos local
db_path = get_db()

# Configuración de la fuente para los botones y etiquetas
font = ("Helvetica", 12)


class InterfazMain(tk.Tk):
    """
    Clase que genera la interfaz principal de inicio de sesión
    y control de viaje.

    Hereda de :class:`tkinter.Tk`.

    Attributes
    ----------
    username : tk.StringVar
        Variable para el nombre de usuario.
    password : tk.StringVar
        Variable para la contraseña.
    gps_thread : threading.Thread
        Hilo encargado de capturar datos GPS.
    stop_event : threading.Event
        Evento para controlar la detención del hilo GPS.
    """
    def __init__(self):
        """
        Inicializa la ventana principal y sus componentes gráficos.
        """
        super().__init__()

        # Inicia en fullscreen, para salir se usa Esc
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda event:
                  self.attributes("-fullscreen", False))

        self.title("INICIO DE SESION")

        # Ajustar a las dimensiones de la pantalla táctil
        self.geometry("800x480")

        self.configure(bg="lightblue")  # Fondo de color azul claro

        # Variables internas de nombre de usuario/contraseña
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.gps_thread = None
        self.stop_event = threading.Event()

        self.create_widgets()

    def create_widgets(self):
        """
        Crea los elementos gráficos de la pantalla de inicio de sesión
        y del control de viaje, incluyendo botones y campos de entrada.
        """
        # Crear un marco para el inicio de sesión
        self.login_frame = tk.Frame(self, bg="lightblue")
        self.login_frame.pack(fill='both')

        # Frame para entradas de usuario y contraseña
        self.user_pass_frame = tk.Frame(self.login_frame, bg="lightblue")
        self.user_pass_frame.pack(pady=20)

        tk.Label(self.user_pass_frame, text="USUARIO:", bg="yellow",
                 font=font).pack(side=tk.LEFT, padx=5)
        tk.Entry(self.user_pass_frame, textvariable=self.username,
                 font=font).pack(side=tk.LEFT, padx=5)

        tk.Label(self.user_pass_frame, text="CONTRASEÑA:", bg="yellow",
                 font=font).pack(side=tk.LEFT, padx=5)
        tk.Entry(self.user_pass_frame, textvariable=self.password,
                 show="*", font=font).pack(side=tk.LEFT, padx=5)

        # Frame para botones de iniciar
        self.inic_frame = tk.Frame(self.login_frame, bg="lightblue")
        self.inic_frame.pack(pady=5)

        tk.Button(self.inic_frame, text="INICIAR", bg="lightgreen",
                  fg="black", font=font,
                  command=self.login).pack(side=tk.LEFT, padx=80)

        # Label para mostrar mensajes de estado de inicio
        self.status_login = tk.StringVar()
        tk.Label(self.login_frame, textvariable=self.status_login,
                 fg="red", font=font).pack(expand=True, pady=1)

        # Crear el teclado y almacenarlo en self.keyboard_frame
        self.keyboard_frame = tk.Frame(self.login_frame, bg="lightblue")
        self.keyboard_frame.pack(expand=True, pady=10)
        self.create_keyboard()

        # Crear un marco para la sección del viaje (inicialmente oculta)
        self.trip_frame = tk.Frame(self, bg="lightblue")

        # Se hacen botones que cambian de color
        self.botonIniciar = tk.Button(self.trip_frame, text="Iniciar Viaje",
                                      bg="lightgreen", fg="black",
                                      font=font, command=self.start_gps,
                                      width=20, height=3)
        self.botonIniciar.pack(pady=20)

        self.botonFinalizar = tk.Button(self.trip_frame, text="Parar Viaje",
                                        bg="yellow", fg="black",
                                        font=font, command=self.stop_gps,
                                        width=20, height=3)
        self.botonFinalizar.pack(pady=20)

        self.botonLogout = tk.Button(self.trip_frame, text="Cerrar sesión",
                                     bg="red", fg="black",
                                     font=font, command=self.logout,
                                     width=20, height=3)
        self.botonLogout.pack(pady=20)

        # Label para mostrar mensajes de estado
        self.status_message = tk.StringVar()
        tk.Label(self.trip_frame, textvariable=self.status_message,
                 font=font, fg="green").pack(expand=True, pady=10)

    def create_keyboard(self):
        """
        Crea un teclado táctil en la pantalla de inicio de sesión.
        """

        # Caracteres del teclado
        keys = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M', '@', '.', '_',
            'ESPACIO', 'BORRAR'
        ]

        keyboard_frame = tk.Frame(self.keyboard_frame, bg="lightblue")
        keyboard_frame.pack(expand=True, pady=20)

        total_columns = 10

        for index, key in enumerate(keys):
            # Colores predeterminados
            if key == 'ESPACIO':
                bg_color = "lightgray"
                fg_color = "black"
            elif key == 'BORRAR':
                bg_color = "red"
                fg_color = "white"
            else:
                bg_color = "black"
                fg_color = "white"

            # Crear el botón con los colores aplicados
            button = tk.Button(
                keyboard_frame,
                text=key,
                width=5,
                font=font,
                bg=bg_color,  # Color de fondo
                fg=fg_color,  # Color del texto
                command=lambda k=key: self.key_press(k)
            )

            # Colocar el botón en la cuadrícula
            if key != 'ESPACIO':
                row, col = divmod(index, total_columns)
                button.grid(row=row, column=col, padx=2, pady=2)

                # Ajustar botón BORRAR
                if key == 'BORRAR':
                    button.config(width=10)
                    button.grid(column=8, columnspan=2, sticky="we")
            else:
                # Ajustar botón ESPACIO
                button.grid(row=row + 1, column=0, columnspan=8,
                            padx=2, pady=2, sticky="we")

    def key_press(self, key):
        """
        Simula el efecto de presionar una tecla en el teclado táctil.

        Parameters
        ----------
        key : str
            Tecla presionada.
        """

        # Se detecta la ventana seleccionada
        focused_widget = self.focus_get()

        # Se genera el comportamiento correspondiente a la tecla.
        if isinstance(focused_widget, tk.Entry):
            if key == "BORRAR":
                current_text = focused_widget.get()
                focused_widget.delete(0, tk.END)
                focused_widget.insert(0, current_text[:-1])
            elif key == "ESPACIO":
                focused_widget.insert(tk.END, " ")
            else:
                focused_widget.insert(tk.END, key)

    def verificar_operador(self, usuario, contraseña):
        """
        Verifica las credenciales ingresadas para el inicio de sesión.
        Se verifica con base de datos local "operadores.db". Se debe modificar
        una vez esté el servidor activo.

        :param usuario: Nombre de usuario ingresado.
        :type usuario: tk.StringVar
        :param contraseña: Contraseña ingresada.
        :type contraseña: tk.StringVar
        :return: Booleano indicando si credenciales son válidos.
        :rtype: Bool
        """

        # Se lee la base de datos local.
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Se busca el conjunto de nombre de usuario y contraseña
        cursor.execute("SELECT * FROM operadores WHERE username = ? \
                       AND password = ?", (usuario, contraseña))

        # Si se encuentra un resultado, se devolverá una fila
        operador = cursor.fetchone()

        # Se imprime mensaje de error si es necesario
        if not operador:
            self.status_login.set("Usuario y/o contraseña inválidos.")

        conn.close()

        if operador:  # Si se encontró un operador
            return operador  # Devuelve los datos del operador
        return None

    def login(self):
        """
        Realiza el proceso de inicio de sesión verificando las credenciales.

        Si es exitoso, envía los datos del operador a la API y muestra la
        interfaz de control de viaje.
        """
        usuario = self.username.get()
        contraseña = self.password.get()
        operador = self.verificar_operador(usuario, contraseña)

        # Una vez se use solo el login con el API se debe quitar este IF
        # y dejar solo el de operador.
        if operador:
            # Si la verificación es exitosa, enviar los datos
            # del operador a la API
            data = {
                "operator_id": operador[0],
                "name": operador[1],
                "phone": operador[2],
                "email": operador[3]
            }
            post_data("AGREGAR EXTENSION", data)

            # Ocultar el marco de inicio de sesión y mostrar el marco del viaje
            self.login_frame.pack_forget()
            self.trip_frame.pack(expand=True, fill='both')

            # Ocultar el teclado después del inicio de sesión
            self.keyboard_frame.pack_forget()

    def logout(self):
        """
        Cierra sesión y regresa a la interfaz de inicio.
        Llama función para finalizar el viaje.
        """
        # Finalizar el viaje
        self.stop_gps()

        # Ocultar el marco del viaje y mostrar el marco de inicio de sesión
        self.trip_frame.pack_forget()
        self.login_frame.pack(expand=True, fill='both')
        self.keyboard_frame.pack(expand=True, fill='both')

    def start_gps(self):
        """
        Inicia la captura de datos por medio de función de
        maejarGPS. Cambia el color de botones de control.
        """

        # Cambia botones de color
        self.botonFinalizar.config(bg="gray")
        self.botonIniciar.config(bg="green")

        # Si ya se encuentra iniciado se notifica
        if self.gps_thread and self.gps_thread.is_alive():
            print("La lectura de GPS ya está en progreso.")
            return

        # Limpiar el evento de parada antes de comenzar
        self.stop_event.clear()

        # Iniciar la lectura de GPS en un hilo separado
        self.gps_thread = threading.Thread(
            target=manejarGPS,
            args=(self.stop_event,),
            # Hacer que el hilo se cierre
            # cuando se cierra el programa principal
            daemon=True
        )
        self.gps_thread.start()
        # Actualizar el mensaje de estado
        self.status_message.set("Lectura de GPS iniciada.")
        print("Lectura de GPS iniciada.")

    def stop_gps(self):
        """Finaliza la captura de datos por medio de función de
        maejarGPS. Cambia el color de botones de control.
        """

        # Cambia color de botones de control
        self.botonFinalizar.config(bg="red")
        self.botonIniciar.config(bg="gray")

        # Si el viaje se encuentra activo
        if self.gps_thread and self.gps_thread.is_alive():
            self.stop_event.set()  # Señalar al hilo que se detenga
            self.gps_thread.join()  # Esperar a que el hilo termine

            # Actualizar el mensaje de estado
            self.status_message.set("Lectura de GPS finalizada.")

        # Si viaje ya estaba finalizado
        else:
            self.status_message.set("La lectura de GPS no está en ejecución.")

    def on_closing(self):
        """
        Cierra la aplicación finalizando correctamente los procesos activos.
        """
        # Asegurarse de que el hilo de GPS se detenga antes de cerrar
        self.stop_gps()
        self.destroy()


if __name__ == "__main__":
    app = InterfazMain()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
