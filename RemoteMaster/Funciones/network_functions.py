# Librerías de red
import nmap
import psutil
import socket
import ipaddress

# Librerías de personalización
from colorama import init, Fore

# Iniciar init para sistemas NT
init()

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