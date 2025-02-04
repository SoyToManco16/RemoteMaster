# Librerías del sistema
from pathlib import Path
from Funciones.system_funcions import clear
import shutil


# Librerias para paramiko
from Funciones.paramiko_functions import key_or_not

# Librerías funciones de red
from Funciones.network_functions import get_interfaces, get_neighbors, get_network_from_interface, show_ips_and_interfaces

# Librerías de personalización
from colorama import Fore

# Librería para los menús
from Menus.menus_rm import main_menu, show_menu_os_type, file_transfer_menu


# Ejecución del programa principal
if __name__ == "__main__":

    # Mostrar menu
    main_menu()

    # Obtener redes
    interfaces_info = get_interfaces()
    show_ips_and_interfaces(interfaces_info)
    print(" ")

    # Pedir dirección IP a el usuario
    chosenet = input(f"{Fore.CYAN}Introduce la dirección IP de la interfaz que vas a utilizar: {Fore.RESET}")

    # Obtener la red de la direccion IP del usuario 
    user_network = get_network_from_interface(chosenet, interfaces_info)
    user_network = str(user_network) # Convertimos a string porque la función de nmap espera un string y no  <class 'ipaddress.IPv4Network'>
    print(" ")
    
    # Obtener equipos conectados de la red del usuario
    net_hosts = get_neighbors(user_network)

    # Introducir la IP a la que nos queremos conectar (Esta variable la pasamos a las funciones de paramiko)
    choosehost = input(f"{Fore.CYAN}Seleccione la dirección IP del host al que quiere conectarse: {Fore.RESET}")

    # Obtener el sistema operativo del host al que nos conectaremos
    host_os_type = input("Introduce el tipo de sistema operativo del host (Windows / Linux): ").strip().lower()

    # Preguntar si el usuario tiene claves en el sistema para realizar conexiones
    claves = input("¿Dispones de claves para estableces las conexiones?: (s/n)").lower()
    sshclient = key_or_not(claves)

    if sshclient == None:
        print(f"{Fore.RED}No se ha podido realizar la conexión, cerrando el programa... {Fore.RESET}")

    # Mostrar el menú según el sistema operativo del host
    show_menu_os_type(host_os_type)

    """ 
    print(Fore.CYAN + rm_windows + Fore.RESET + "\n")
    print("1. Transferencia de archivos (SFTP)")
    print("2. Shell (SSH, WinRM)")
    print("3. Interfaz gráfica (MTSMC)")



    print(Fore.YELLOW + rm_linux + Fore.RESET + "\n")
    print("1. Transferencia de archivos (SFTP)")
    print("2. Shell (SSH)")
    """

    # Obtener la opción del usuario
    answer = input("Introduce una opción: ").strip()

    # Manejar la opción seleccionada
    if answer == "1":  # Transferencia de archivos
        file_transfer_menu()
    elif answer == "2" and host_os_type == "linux":  # Shell SSH en Linux
        print("Abriendo shell SSH (pendiente de implementación).")
    elif answer == "2" and host_os_type == "windows":  # Shell SSH/WinRM en Windows
        print("Abriendo shell SSH/WinRM (pendiente de implementación).")
    elif answer == "3" and host_os_type == "windows":  # Interfaz gráfica (Windows)
        print("Abriendo interfaz gráfica MTSMC (pendiente de implementación).")
    else:
        print("Opción inválida.")


    


    


   