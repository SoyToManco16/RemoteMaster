# Librerias
from colorama import Fore
from Menus.ascii_art import ascii_art, rm_windows, rm_linux, rm_hybrid, rm_IPOnly
from Funciones.system_funcions import get_os
from Funciones.paramiko_functions import start_ssh

# Get os
myhost = get_os()
myhost = myhost.lower()

# Menús
def main_menu():
    print(Fore.CYAN + ascii_art)
    print(f"Sistema en uso: {Fore.WHITE} {myhost} {Fore.RESET}")

def show_menu_os_type(remote_os_type, host_os_type):
    """Muestra el menú adecuado según el sistema operativo del host."""
    # Pasar a minúsculas para evitar confrontación
    remote_os_type = remote_os_type.lower()
    host_os_type = host_os_type.lower()

    if remote_os_type == "windows" and host_os_type == "windows":
        windows_to_windows_menu()    
    elif remote_os_type == "linux" and host_os_type == "linux":
        linux_to_linux_menu()
    elif (remote_os_type == "linux" and host_os_type == "windows") or (remote_os_type == "windows" and host_os_type == "linux"):
        hybrid_menu()
    elif (remote_os_type == "ip" and ((host_os_type == "windows") or (host_os_type == "linux"))):
        only_IP_menu()
    else:
        print(f"No hay soporte para: {remote_os_type.capitalize()}")
        exit()

def windows_to_windows_menu():
    """Muestra el menú para Windows."""

    print(Fore.CYAN + rm_windows + "\n")
    print(f"Sistema en uso: {Fore.RESET}{myhost}")
    print(f"{Fore.CYAN}1. Transferencia de archivos (SFTP)")
    print("2. Shell (SSH, WinRM)")
    print(f"3. Interfaz gráfica (MTSMC) {Fore.RESET}")

def linux_to_linux_menu():
    """Muestra el menú para Linux."""

    print(Fore.YELLOW + rm_linux + "\n")
    print(f"Sistema en uso: {Fore.RESET}{myhost}")
    print(f"{Fore.YELLOW}1. Transferencia de archivos (SFTP)")
    print(f"2. Shell (SSH){Fore.RESET}")


def hybrid_menu():
    """Muestra el menú de Windows a Linux o de Linux a Windows."""

    print(Fore.GREEN + rm_hybrid + Fore.RESET + "\n")
    print(f"{Fore.GREEN}Sistema en uso: {Fore.RESET}{myhost}")
    print(f"{Fore.GREEN}1. Transferencia de archivos (SFTP)")
    print(f"2. Shell (SSH) {Fore.RESET}")


def only_IP_menu():
    """Muestra un menú para conexiones de las que solo se conoce la IP"""

    print(Fore.LIGHTRED_EX + rm_IPOnly + Fore.RESET + "\n")
    print(f"{Fore.LIGHTRED_EX}Sistema en uso: {Fore.RESET}{myhost}")
    print(f"{Fore.LIGHTRED_EX}1. Transferencia de archivos (SFTP)")
    print(f"2. Shell (SSH) {Fore.RESET}")


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
        remote_dir = input("Introduce el directorio remoto del servidor: ")
        local_file = input("Introduce el fichero o ficheros que quieres descargarte: ")
        sftp_upload_files(local_file, remote_dir)

    else:
        print("Opción inválida.")

# Menús para windows (RDP Y WinRM)
def shell_windows():
    """Submenú para elegir entre conexión mediante WinRM (PowerShell) o SSH."""
    from MainRemote import sshclient # Variable para realizar conexiones ssh

    print("\n¿Qué tipo de conexión deseas realizar?")
    print("1. WinRM (Debes de haber ejecutado previamente RM-Winrm.ps1 !!)")
    print("2. SSH")

    option = input("Introduce una opción: ")

    if option == "1":
        call_winrm()
    elif option == "2":
        start_ssh(sshclient)
    else:
        print(f"{Fore.RED}Opción no válida, saliendo del programa... {Fore.RESET}")