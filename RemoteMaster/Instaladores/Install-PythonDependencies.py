import subprocess
import sys

# Lista de librerías a instalar
librerias = [
    'python-nmap',
    'psutil',
    'paramiko',
    'colorama',
    'pyautogui'
]

# Función para instalar las librerías
def instalar_librerias():
    try:
        for libreria in librerias:
            print(f"Instalando {libreria}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', libreria])
        print("Todas las librerías se han instalado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Hubo un error al instalar una librería: {e}")

# Ejecutar la instalación
if __name__ == "__main__":
    instalar_librerias()
