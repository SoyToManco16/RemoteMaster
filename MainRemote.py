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

def show_menu_os_type(ostype_host):

    if ostype_host == "Windows":
        print(Fore.CYAN + rm_windows + Fore.RESET + "\n")
        print("1. File Transfer (FTP, SFTP)")
        print("2. Shell (SSH, WinRM)")
        print("3. Interfaz gráfica (MTSMC)")

    else:
        print(Fore.YELLOW + rm_linux + Fore.RESET + "\n")
        print("1. File Transfer (FTP, SFTP)")
        print("2. Shell (SSH)")
    



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

    choosehost = input(f"{Fore.CYAN}Seleccione la dirección IP del host al que quiere conectarse: {Fore.RESET}")
    host_os_type = input("Introduce el tipo de sistema operativo de el host: (Windows / Linux): ")
    clear()

    show_menu_os_type(host_os_type)
    


    


   
