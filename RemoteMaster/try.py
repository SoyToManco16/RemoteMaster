import nmap
import psutil
import socket
import ipaddress
from colorama import Fore

def get_neighbors(network_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=network_range, arguments='-O')

    print(f"{Fore.YELLOW}Hosts encontrados{Fore.RESET}\n")

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
    print("\n" + f"{Fore.YELLOW}Interfaces del sistema{Fore.RESET}\n")
    
    for interface, (ip_address, netmask) in net_info.items():
        print(f"{Fore.LIGHTYELLOW_EX}Interfaz: {interface} - Dirección IP: {ip_address} - Máscara de red: {netmask}{Fore.RESET}\n")

def get_network_from_interface(ip, net_info):
    for _, (interface_ip, mask) in net_info.items():
        if interface_ip == ip:
            return ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
    return None

# Ejecución del menú principal
if __name__ == "__main__":
    # Obtener redes
    interfaces_info = get_interfaces()
    show_ips_and_interfaces(interfaces_info)
    print(" ")

    # Pedir IP a utilizar para convertir a red y escanear con nmap para obtener sistemas disponibles
    chosenet = input(f"{Fore.CYAN}Introduce la dirección IP de la interfaz que vas a utilizar: {Fore.RESET}")

    user_network = get_network_from_interface(chosenet, interfaces_info)
    user_network = str(user_network)  # Convertimos a string porque la función de nmap espera un string y no  <class 'ipaddress.IPv4Network'>
    print(" ")
    
    # Obtener equipos conectados de la red del usuario y sus sistemas operativos
    get_neighbors(user_network)