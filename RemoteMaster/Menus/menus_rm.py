# Librerias
from colorama import Fore
from Menus.ascii_art import ascii_art, rm_windows, rm_linux
from Funciones.system_funcions import get_os

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
    print("1. Transferencia de archivos (SFTP)")
    print("2. Shell (SSH, WinRM)")
    print("3. Interfaz gráfica (MTSMC)")

def linux_menu():
    """Muestra el menú para Linux."""
    print(Fore.YELLOW + rm_linux + Fore.RESET + "\n")
    print("1. Transferencia de archivos (SFTP)")
    print("2. Shell (SSH)")



# Menús File Transfer

def file_transfer_menu():
    """Menú principal para transferencia de archivos."""
    print("\n¿Qué tipo de transmisión desea utilizar?")
    print("1. Transferencia simple (Subir/Descargar)")
    print("2. Abrir terminal")

    option = input("Seleccione una opción (1/2): ")

    if option == "1":
        file_transfer_type_simple_menu()
    elif option == "2":
        open_sftp_shell()
    else:
        print("Eso no es una opción correcta")

def file_transfer_type_simple_menu():
    """Submenú para descarga o subida de archivos en transferencia simple."""
    print("\n¿Qué tipo de transferencia deseas realizar?")
    print("1. Descargar un fichero o varios")
    print("2. Subir un fichero o varios")

    option = input("Seleccione una opción (1/2): ").strip()

    if option == "1":
        remote_dir = input("Introduce el directorio remoto del servidor: ")
        local_file = input("Introduce el fichero o ficheros que quieres descargarte: ")
        sftp_download_files(local_file, remote_dir)

    elif option == "2":
        print(f"Subiendo archivo con {protocol} (pendiente de implementación).")
    else:
        print("Opción inválida.")

