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

# Librerías del sistema
from pathlib import Path
import os
import shutil

# Librerías de red
import nmap
import psutil
import socket
import ipaddress
import paramiko

# Librerías de personalización
from colorama import Fore

# Variables explícitas para menús
answer = 0

# Funciones

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


# Funciones de sistema

def get_os():
    ostype = os.name

    if ostype == 'nt':
        return "Windows"
    else:
        return "Linux"
    
current_os = get_os()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Funciones de red

def get_neighbors(network_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=network_range, arguments='-O')

    print(f"{Fore.YELLOW}Hosts encontrados{Fore.RESET}\n")

    # Verificar si se encontraron hosts
    if not nm.all_hosts():
        print(f"{Fore.RED}No se han encontrado hosts en la red, RemoteHost no puede conectarse a algo que no existe... {Fore.RESET}")
        exit()

    # Si se encuentran hosts, mostrar información
    for host in nm.all_hosts():
        if nm[host].state() == "up":
            print(f"{Fore.LIGHTYELLOW_EX}Host encontrado:{Fore.RESET} {host}")
            if 'osclass' in nm[host]:
                for osclass in nm[host]['osclass']:
                    print(f"{Fore.LIGHTYELLOW_EX}Sistema Operativo: {osclass['osfamily']} {osclass['osgen']}{Fore.RESET}")
            elif 'osmatch' in nm[host]:
                for osmatch in nm[host]['osmatch']:
                    print(f"{Fore.LIGHTYELLOW_EX}Sistema Operativo: {osmatch['name']} ({osmatch['accuracy']}% accuracy){Fore.RESET}")
            else:
                print(f"{Fore.LIGHTYELLOW_EX}Sistema Operativo: No detectado{Fore.RESET}")



def get_interfaces():
    interfaces = psutil.net_if_addrs()
    net_info = {}

    for interface, addrs in interfaces.items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                net_info[interface] = (addr.address, addr.netmask)

    return net_info

def show_ips_and_interfaces(net_info):

    """Muestra las interfaces disponibles con su IP y máscara de subred."""
    net_info = get_interfaces()
    
    print("\n" + f"{Fore.YELLOW}Interfaces del sistema{Fore.RESET}\n")
    
    for interface, (ip_address, netmask) in net_info.items():  # Se desempaca correctamente la tupla
        print(f"{Fore.LIGHTYELLOW_EX}Interfaz: {interface} - Dirección IP: {ip_address} - Máscara de red: {netmask}{Fore.RESET}\n")

def get_network_from_interface(ip, net_info):
    for _, (interface_ip, mask) in net_info.items():
        if  interface_ip == ip:
            return ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
    return None


    

# Ejecución del menú principal
if __name__ == "__main__":

    # Mostrar menu
    main_menu()

    # Obtener redes
    interfaces_info = get_interfaces()
    show_ips_and_interfaces(interfaces_info)
    print(" ")

    # Pedir IP a utilizar para convertir a red y escanear con nmap para obtener sistemas disponibles
    chosenet = input(f"{Fore.CYAN}Introduce la dirección IP de la interfaz que vas a utilizar: {Fore.RESET}")

    user_network = get_network_from_interface(chosenet, interfaces_info)
    user_network = str(user_network) # Convertimos a string porque la función de nmap espera un string y no  <class 'ipaddress.IPv4Network'>
    print(" ")
    
    # Obtener equipos conectados de la red del usuario
    net_hosts = get_neighbors(user_network)

    # Introducir la IP a la que nos queremos conectar y el tipo de sistema operativo de la IP
    choosehost = input(f"{Fore.CYAN}Seleccione la dirección IP del host al que quiere conectarse: {Fore.RESET}")

    # Obtener el sistema operativo del host al que nos conectaremos
    host_os_type = input("Introduce el tipo de sistema operativo del host (Windows / Linux): ").strip().lower()

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


    


    


   
