#!/bin/bash

# Nombre del archivo requirements.txt
requirements="requirements.txt"

# Función para instalar paquetes usando pip
install_with_pip() {
    echo "Instalando paquetes con pip"
    python3 -m pip install -r "$requirements" --user
}

# Función para instalar paquetes usando apt (si pip falla)
install_with_apt() {
    echo "Intentando instalar con apt"
    while IFS= read -r package; do
        # Asegúrate de que el paquete no esté vacío
        if [[ ! -z "$package" ]]; then
            echo "Instalando $package con apt..."
            sudo apt-get install -y python3-"$package"
        fi
    done < "$requirements"
}

# Verificar si el archivo requirements.txt existe
if [[ ! -f "$requirements" ]]; then
    echo "El archivo $requirements no existe. Asegúrate de que esté presente."
    exit 1
fi

# Intentar instalar con pip
install_with_pip

# Verificar si hubo error en la instalación con pip
if [[ $? -ne 0 ]]; then
    echo "Error al instalar con pip. Probando con apt..."
    sleep 1
    clear
    install_with_apt
    echo "Ya puedes usar RemoteMaster !!"
else 
    echo "Ya puedes usar RemoteMaster !!"
fi
