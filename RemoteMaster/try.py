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
        shell.close()
        ssh_client.close()


hostname = "192.168.56.108"
port = 22
username = "miguel"
password = "Micasa123"

sshclient = create_ssh_client_pass(hostname, port, username, password)

start_ssh(sshclient)
