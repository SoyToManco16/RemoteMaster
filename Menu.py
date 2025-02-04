# Librerías del sistema
import os
import shutil
from pathlib import Path

# Librerías de red
import nmap
import psutil
import socket
import ipaddress
import paramiko

# Librerías de personalización
from colorama import Fore

# ASCII Art
ascii_art = r"""
 ____                      _       __  __           _            
|  _ \ ___ _ __ ___   ___ | |_ ___|  \/  | __ _ ___| |_ ___ _ __ 
| |_) / _ \ '_ ` _ \ / _ \| __/ _ \ |\/| |/ _` / __| __/ _ \ '__|
|  _ <  __/ | | | | | (_) | ||  __/ |  | | (_| \__ \ ||  __/ |   
|_| \_\___|_| |_| |_|\___/ \__\___|_|  |_|\__,_|___/\__\___|_|   
"""

rm_windows = r"""
 ____  __  __    __        ___           _                   
|  _ \|  \/  |   \ \      / (_)_ __   __| | _____      _____ 
| |_) | |\/| |____\ \ /\ / /| | '_ \ / _` |/ _ \ \ /\ / / __|
|  _ <| |  | |_____\ V  V / | | | | | (_| | (_) \ V  V /\__ \
|_| \_\_|  |_|      \_/\_/  |_|_| |_|\__,_|\___/ \_/\_/ |___/
"""

rm_linux = r"""
 ____  __  __       _     _                  
|  _ \|  \/  |     | |   (_)_ __  _   ___  __
| |_) | |\/| |_____| |   | | '_ \| | | \ \/ /
|  _ <| |  | |_____| |___| | | | | |_| |>  < 
|_| \_\_|  |_|     |_____|_|_| |_|\__,_/_/\_\ 
"""

# ------------------------ FUNCIONES PARA MENÚS ------------------------

def show_menu_os_type(ostype_host):
    """Muestra el menú adecuado según el sistema operativo del host."""
    if ostype_host == "windows":
        windows_menu()    
    elif ostype_host == "linux":
        linux_menu()
    else:
        print(f"No hay soporte para: {ostype_host.capitalize()}")
        exit(1)

def windows_menu():
    """Muestra el menú para Windows."""
    print(Fore.CYAN + rm_windows + Fore.RESET + "\n")
    print("1. Transferencia de archivos (FTP, SFTP)")
    print("2. Shell (SSH, WinRM)")
    print("3. Interfaz gráfica (MTSMC)")

def linux_menu():
    """Muestra el menú para Linux."""
    print(Fore.YELLOW + rm_linux + Fore.RESET + "\n")
    print("1. Transferencia de archivos (FTP, SFTP)")
    print("2. Shell (SSH)")

# ------------------------ MENÚ DE TRANSFERENCIA DE ARCHIVOS ------------------------

def file_transfer():
    """Menú principal para transferencia de archivos."""
    print("\n¿Qué protocolo desea usar?")
    print("1. FTP (Menos seguro)")
    print("2. SFTP (Más seguro)")

    option = input("Seleccione una opción (1/2): ").strip()

    if option == "1":
        file_transfer_type("FTP")
    elif option == "2":
        file_transfer_type("SFTP")
    else:
        print("Opción inválida. Regresando al menú principal.")

def file_transfer_type(protocol):
    """Menú de tipos de transferencia de archivos."""
    print(f"\nHas elegido {protocol}. ¿Qué tipo de transferencia deseas realizar?")
    print("1. Transferencia simple (Subir/Descargar)")
    print("2. Abrir terminal")

    option = input("Seleccione una opción (1/2): ").strip()

    if option == "1":
        file_transfer_type_simple(protocol)
    elif option == "2":
        print(f"Abrir terminal de {protocol} (pendiente de implementación).")
    else:
        print("Opción inválida.")

def file_transfer_type_simple(protocol):
    """Submenú para descarga o subida de archivos en transferencia simple."""
    print("\n¿Qué tipo de transferencia deseas realizar?")
    print("1. Descargar un fichero")
    print("2. Subir un fichero")

    option = input("Seleccione una opción (1/2): ").strip()

    if option == "1":
        print(f"Descargando archivo con {protocol} (pendiente de implementación).")
    elif option == "2":
        print(f"Subiendo archivo con {protocol} (pendiente de implementación).")
    else:
        print("Opción inválida.")

# ------------------------ FLUJO PRINCIPAL ------------------------

# Obtener el sistema operativo del host al que nos conectaremos
host_os_type = input("Introduce el tipo de sistema operativo del host (Windows / Linux): ").strip().lower()

# Limpiar la pantalla (solo si es compatible con el sistema)
os.system('cls' if os.name == 'nt' else 'clear')

# Mostrar el menú según el sistema operativo del host
show_menu_os_type(host_os_type)

# Obtener la opción del usuario
answer = input("Introduce una opción: ").strip()

# Manejar la opción seleccionada
if answer == "1":  # Transferencia de archivos
    file_transfer()
elif answer == "2" and host_os_type == "linux":  # Shell SSH en Linux
    print("Abriendo shell SSH (pendiente de implementación).")
elif answer == "2" and host_os_type == "windows":  # Shell SSH/WinRM en Windows
    print("Abriendo shell SSH/WinRM (pendiente de implementación).")
elif answer == "3" and host_os_type == "windows":  # Interfaz gráfica (Windows)
    print("Abriendo interfaz gráfica MTSMC (pendiente de implementación).")
else:
    print("Opción inválida.")
