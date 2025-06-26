#!/bin/bash

# Modificar a "true" si el setup es para la Raspberry Pi
RPI=false

# Editar esta variable según el nombre del script con la interfaz
INTERFAZ="main.py"

# Se usa el directorio donde se encuentra el script (gpsTCU)
# como el directorio base.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$SCRIPT_DIR/src/launchInterfaz.sh"
PYTH="$SCRIPT_DIR/src/$INTERFAZ"
VENV_DIR="$SCRIPT_DIR/venv"
AUTO_PATH="/home/$USER/.config/autostart"
AUTO_FILE="$AUTO_PATH/autoBusGPS.desktop"

# Se crean los directorios si no existen
mkdir -p "$AUTO_PATH"

# Se crea enviroment virtual si no existe
if [ ! -d "$VENV_DIR" ]; then
    sudo apt install python3.11-venv
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$SCRIPT_DIR/requirements.txt"
deactivate

if [ "$RPI" = true ]; then
# Se crea el script que ejecuta la interfaz.
cat > "$SCRIPT" << EOF
#!/bin/bash
export DISPLAY=:0

cd "$SCRIPT_DIR" || exit 1
source "$VENV_DIR/bin/activate"
python3 "$PYTH"
EOF

# Se da permisos de ejecución al script.
chmod +x "$SCRIPT"
chmod +x "$PYTH"

# Se crea archivo .desktop que se agrega a autostart.
cat > "$AUTO_FILE" << EOF
[Desktop Entry]
Type=Application
Name=Autostart interfaz de aplicación GPS TCU.
Exec="$SCRIPT"
EOF
fi

echo "Setup finalizado."
