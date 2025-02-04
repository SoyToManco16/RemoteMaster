# Libreías
import os

# Funciones de sistema

def get_os():
    ostype = os.name

    if ostype == 'nt':
        return "Windows"
    else:
        return "Linux"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')