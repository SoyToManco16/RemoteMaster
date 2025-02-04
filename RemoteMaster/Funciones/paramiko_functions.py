# Librerías
import paramiko
from colorama import Fore
import sys
import select
from Funciones.system_funcions import get_os

myhost = get_os()
myhost = myhost.lower()

if myhost == "windows":
    import msvcrt
else:
    import termios
    import tty

# Funciones
def create_ssh_client_pass(hostname, port, username, password):
    try:
        # Crear cliente
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conectar al servidor
        ssh_client.connect(hostname=hostname, port=port, username=username, password=password)

        return ssh_client

    except Exception:
        return None

def create_ssh_client_keys(hostname, port, username, key_file, key_passphrase=None):
    try:
        # Crear cliente
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Cargar la clave privada
        private_key = paramiko.RSAKey(filename=key_file, password=key_passphrase)
        ssh_client.connect(hostname, port, username, pkey=private_key)

        return ssh_client

    except Exception:        
        return None

def key_or_not(host, answer):

    print(f"\n{Fore.YELLOW}Toma de datos para creación de clientes SSH{Fore.RESET}")
    print(f"{Fore.YELLOW}IP del host remoto: {host}{Fore.RESET}")

    hostname = host
    port = int(input(f"{Fore.CYAN}Selecciona el puerto del servidor al que te conectarás (pred: 22): {Fore.RESET}") or "22")
    username = input(f"{Fore.CYAN}Introduce el nombre de usuario con el que te conectarás al servidor: {Fore.RESET}")

    if answer == "s":
        key_file = input(f"{Fore.CYAN}Introduce la ruta del archivo de clave privada: {Fore.RESET}")
        key_passphrase = input(f"{Fore.CYAN}Introduce la frase de paso de la clave privada (si no tiene, deja vacío): {Fore.RESET}") or None
        ssh_client = create_ssh_client_keys(hostname, port, username, key_file, key_passphrase)
        return ssh_client
    
    else:
        password = input(f"{Fore.CYAN}Introduce la contraseña del usuario: {Fore.RESET}")
        ssh_client = create_ssh_client_pass(hostname, port, username, password)
        return ssh_client

def start_ssh(ssh_client):
    if ssh_client is None:
        print(f"{Fore.RED}No existe un cliente SSH, saliendo del programa... {Fore.RESET}")
        exit()

    try:
        shell = ssh_client.invoke_shell()
        print(f"{Fore.GREEN}Sesión SSH interactiva establecida{Fore.RESET}")

        if sys.platform.startswith("win"):  # Si es Windows
            while True:
                if shell.recv_ready():
                    data = shell.recv(1024).decode()
                    if data:
                        print(data, end="")

                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key == b'\r':  # Enter
                        shell.send('\n')
                    elif key == b'\x03':  # Ctrl+C
                        break
                    else:
                        shell.send(key.decode())

        else:  # Si es Linux o macOS
            old_tty_settings = termios.tcgetattr(sys.stdin)
            try:
                tty.setraw(sys.stdin.fileno())
                shell.settimeout(0.0)

                while True:
                    r, w, e = select.select([shell, sys.stdin], [], [])

                    if shell in r:
                        try:
                            output = shell.recv(1024).decode('utf-8')
                            if len(output) == 0:
                                print("\nConexión cerrada")
                                break
                            sys.stdout.write(output)
                            sys.stdout.flush()
                        except Exception as e:
                            print(f"Error recibiendo datos: {e}")
                            break

                    if sys.stdin in r:
                        input_cmd = sys.stdin.read(1)
                        if len(input_cmd) == 0:
                            break
                        shell.send(input_cmd)

            finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty_settings)

    except KeyboardInterrupt:
        print("\nCerrando sesión SSH...")

    finally:
        # Verifica si 'shell' es válido antes de cerrarlo
        if 'shell' in locals() and shell:
            shell.close()

        # Cierra el cliente SSH si está abierto
        if ssh_client.get_transport() is not None:
            ssh_client.close()

