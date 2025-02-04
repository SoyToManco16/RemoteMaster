# Librerias
from colorama import Fore
from ascii_art import ascii_art, rm_windows, rm_linux
from system_funcions import get_os

# Menús
def main_menu():
    print(Fore.CYAN + ascii_art)
    print(f"Sistema en uso: {Fore.WHITE} {get_os()} {Fore.RESET}")

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

# Menús File Transfer

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