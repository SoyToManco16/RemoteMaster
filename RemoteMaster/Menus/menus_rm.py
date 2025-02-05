# Librerias
from colorama import Fore
from Menus.ascii_art import ascii_art, rm_windows, rm_linux, rm_hybrid, rm_IPOnly, rm_sftp, rm_wsman
from Funciones.system_funcions import get_os, clear
from Funciones.paramiko_functions import start_ssh, open_sftp_shell, sftp_download_file, sftp_upload_file
from Funciones.shell_windows_functions import start_winrm_interactive_session, exec_command_with_winrm

# Get os
myhost = get_os()
myhost = myhost.lower()


# Menús
def main_menu():
    print(Fore.CYAN + ascii_art)
    print(f"Sistema en uso: {Fore.WHITE} {myhost} {Fore.RESET}")

def show_menu_os_type(remote_os_type, host_os_type):
    """Muestra el menú adecuado según el sistema operativo del host."""
    # Convertir a minúsculas para evitar problemas
    remote_os_type = remote_os_type.lower()
    host_os_type = host_os_type.lower()

    if remote_os_type == "windows" and host_os_type == "windows":
        windows_to_windows_menu()    
    elif remote_os_type == "linux" and host_os_type == "linux":
        linux_to_linux_menu()
    elif (remote_os_type == "linux" and host_os_type == "windows") or (remote_os_type == "windows" and host_os_type == "linux"):
        hybrid_menu()
    elif remote_os_type == "ip" and host_os_type in ["windows", "linux"]:
        only_IP_menu()
    else:
        print(f"{Fore.RED}No hay soporte para: {remote_os_type.capitalize()} o combinación inválida.{Fore.RESET}")
        exit()
        
def windows_to_windows_menu():
    """Muestra el menú para Windows."""

    print(Fore.CYAN + rm_windows + "\n")
    print(f"Sistema en uso: {Fore.RESET}{myhost}")
    print(f"{Fore.CYAN}1. Transferencia de archivos (SFTP)")
    print("2. Shell (SSH, WinRM)")
    print(f"3. Interfaz gráfica (MSTSC) {Fore.RESET}")

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

def file_transfer_menu(sshclient, sftp_client):
    clear()
    """Menú principal para transferencia de archivos."""

    print(Fore.LIGHTMAGENTA_EX + rm_sftp + "\n")
    print("\n¿Qué tipo de transmisión desea utilizar?")
    print("1. Transferencia simple (Subir/Descargar)")
    print("2. Abrir terminal")

    option = input(f"Seleccione una opción (1/2):{Fore.RESET} ")

    if option == "1":
        file_transfer_type_simple_menu(sftp_client)
    elif option == "2":
        open_sftp_shell(sshclient)
    else:
        print(f"{Fore.RED}Opción no válida, saliendo de RemoteMaster... {Fore.RESET}")
        exit()


def file_transfer_type_simple_menu(sftp_client):
    """Submenú para descarga o subida de archivos en transferencia simple."""

    # Mostramos el menú para seleccionar el tipo de transferencia
    print(f"\n{Fore.LIGHTMAGENTA_EX}¿Qué tipo de transferencia deseas realizar?{Fore.RESET}")
    print(f"{Fore.LIGHTMAGENTA_EX}1. Descargar un fichero{Fore.RESET}")
    print(f"{Fore.LIGHTMAGENTA_EX}2. Subir un fichero{Fore.RESET}")
    
    # Pedimos al usuario que seleccione una opción
    option = input(f"{Fore.LIGHTMAGENTA_EX}Seleccione una opción (1/2): {Fore.RESET}").strip()

    # Validamos la opción seleccionada
    if option == "1":
        # Si seleccionó descargar, pedimos la ruta remota y local
        remote_file = input(f"{Fore.LIGHTMAGENTA_EX}Introduce la ruta completa del fichero remoto que deseas descargar: {Fore.RESET}").strip()
        local_file = input(f"{Fore.LIGHTMAGENTA_EX}Introduce la ruta completa donde deseas guardar el fichero en tu máquina local: {Fore.RESET}").strip()
        print("")
        
        # Llamamos a la función de descarga
        sftp_download_file(sftp_client, remote_file, local_file)

    elif option == "2":
        # Si seleccionó subir, pedimos las rutas
        local_file = input(f"{Fore.LIGHTMAGENTA_EX}Introduce la ruta completa del fichero local que deseas subir: {Fore.RESET}").strip()
        remote_file = input(f"{Fore.LIGHTMAGENTA_EX}Introduce la ruta completa donde deseas subir el fichero en el servidor remoto: {Fore.RESET}").strip()
        print("")
        
        # Llamamos a la función de subida
        sftp_upload_file(sftp_client, local_file, remote_file)

    else:
        # Si la opción no es válida, mostramos un mensaje y salimos
        print(f"{Fore.RED}Opción no válida, saliendo de RemoteMaster...{Fore.RESET}")
        exit()

# Menú para windows (SSH Y WinRM)
def shell_windows(ssh_client, hostname, username, password):
    """Submenú para elegir entre conexión mediante WinRM (PowerShell) o SSH."""

    print(f"\n{Fore.CYAN}¿Qué tipo de conexión deseas realizar?")
    print("1. WinRM")
    print("2. SSH")

    option = input(f"Introduce una opción:{Fore.RESET} ")

    if option == "1":
        call_winrm(hostname, username, password)
    elif option == "2":
        start_ssh(ssh_client)
    else:
        print(f"{Fore.RED}Opción no válida, saliendo del programa... {Fore.RESET}")
        exit()

def call_winrm(hostname, username, password):
    """ Submenú para WinRM para elegir entre ejecutar un comando solo 
    o sesión interactiva """

    clear()
    print(Fore.CYAN + rm_wsman + "\n")
    print("1. Ejecutar un comando por WinRM")
    print("2. Abrir terminal (PowerShell)")

    option = input(f"Introduce una opción:{Fore.RESET} ")

    if option == "1":
        comando = input(f"Introduce el comando que quieres ejecutar en {hostname}")
        exec_command_with_winrm(comando, hostname, username, password)
    elif option == "2":
        start_winrm_interactive_session(hostname, username, password)
    else:
        print(f"{Fore.RED}Opción no válida, saliendo del programa... {Fore.RESET}")
        exit()