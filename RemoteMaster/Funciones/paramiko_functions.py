# Librerías
from MainRemote import choosehost
import paramiko
from colorama import Fore

# Funciones
def create_ssh_client_pass(hostname, port, username, password):
    try:
        # Crear cliente
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conectar al servidor
        ssh_client.connect(hostname=hostname, port=port, username=username, password=password)
        print(f"{Fore.GREEN}Cliente creado en {hostname}{Fore.RESET}")

        return ssh_client

    except Exception as e:
        print(f"Error: {e}")
        ssh_client = None
        return ssh_client 

def create_ssh_client_keys(hostname, port, username, key_file, key_passphrase=None):
    try:
        # Crear cliente
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Cargar la clave privada
        private_key = paramiko.RSAKey(filename=key_file, password=key_passphrase)
        ssh_client.connect(hostname, port, username, pkey=private_key)
        print(f"{Fore.GREEN}Cliente creado en {hostname}{Fore.GREEN}")

        return ssh_client

    except Exception as e:
        print(f"Error: {e}")
        ssh_client = None
        return ssh_client 

def key_or_not(answer):

    print(f"{Fore.YELLOW}Toma de datos para creación de clientes SSH{Fore.RESET}")

    print(f"{Fore.YELLOW}IP del host remoto: {choosehost}{Fore.RESET}")

    hostname = choosehost
    port = int(input(f"{Fore.CYAN}Selecciona el puerto del servidor al que te conectarás (pred: 22): {Fore.RESET}") or "22")
    username = input(f"{Fore.CYAN}Introduce el nombre de usuario con el que te conectarás al servidor: {Fore.RESET}")

    if answer == "s":
        key_file = input(f"{Fore.CYAN}Introduce la ruta del archivo de clave privada: {Fore.RESET}")
        key_passphrase = input(f"{Fore.CYAN}Introduce la frase de paso de la clave privada (si no tiene, deja vacío): {Fore.RESET}") or None
        ssh_client = create_ssh_client_keys(hostname, port, username, key_file, key_passphrase)
    else:
        password = input(f"{Fore.CYAN}Introduce la contraseña del usuario: {Fore.RESET}")
        ssh_client = create_ssh_client_pass(hostname, port, username, password)



