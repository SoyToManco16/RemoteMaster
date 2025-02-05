# Librerías
import paramiko
from colorama import Fore
from Funciones.system_funcions import get_os

myhost = get_os()
myhost = myhost.lower()

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


def start_sftp_interactive(ssh_client):
    if ssh_client is None:
        print("No existe un cliente SSH, saliendo del programa...")
        exit()

    try:
        sftp_client = ssh_client.open_sftp()
        print("Conexión SFTP interactiva establecida.")

        # Intentamos establecer el directorio raíz al inicio
        try:
            sftp_client.chdir('/')  # Cambia al directorio raíz
            current_directory = sftp_client.getcwd()  # Obtén el directorio actual
            print(f"Directorio actual: {current_directory}")
        except Exception as e:
            print(f"Error al establecer el directorio raíz: {e}")
            current_directory = "/"

        while True:
            # Mostrar el prompt interactivo con el directorio actual
            print(f"\nsftp ({current_directory})> ", end="")
            command = input().strip()

            # Salir de la sesión SFTP
            if command == "exit" or command == "quit":
                print("Saliendo de la sesión SFTP...")
                break

            # Subir archivo
            elif command.startswith("put "):
                parts = command.split(" ", 2)
                if len(parts) < 3:
                    print("Uso: put <archivo_local> <archivo_remoto>")
                    continue

                local_file = parts[1]
                remote_path = parts[2]

                try:
                    sftp_client.put(local_file, remote_path)
                    print(f"Archivo subido a {remote_path}")
                except Exception as e:
                    print(f"Error al subir archivo: {e}")

            # Descargar archivo
            elif command.startswith("get "):
                parts = command.split(" ", 2)
                if len(parts) < 3:
                    print("Uso: get <archivo_remoto> <archivo_local>")
                    continue

                remote_file = parts[1]
                local_path = parts[2]

                try:
                    sftp_client.get(remote_file, local_path)
                    print(f"Archivo descargado a {local_path}")
                except Exception as e:
                    print(f"Error al descargar archivo: {e}")

            # Listar archivos remotos
            elif command == "ls":
                try:
                    files = sftp_client.listdir(current_directory)
                    for file in files:
                        print(file)
                except Exception as e:
                    print(f"Error al listar archivos: {e}")

            # Cambiar el directorio remoto (similar a cd)
            elif command.startswith("cd "):
                path = command[3:].strip()
                try:
                    sftp_client.chdir(path)
                    current_directory = sftp_client.getcwd()  # Actualiza el directorio actual
                    print(f"Directorio cambiado a: {current_directory}")
                except Exception as e:
                    print(f"Error al cambiar el directorio: {e}")

            # Mostrar el directorio actual remoto (similar a pwd)
            elif command == "pwd":
                print(f"Directorio actual: {current_directory}")

            # Comandos no reconocidos
            else:
                print(f"Comando no reconocido: {command}")
                print("Comandos disponibles: put, get, ls, cd, pwd, exit")

    except Exception as e:
        print(f"Error al iniciar sesión SFTP: {e}")
    finally:
        sftp_client.close()

    


hostname = "192.168.56.1"
port = 22
username = "miguel"
password = "Micasa35262441"

sshclient = create_ssh_client_pass(hostname, port, username, password)

start_sftp_interactive(sshclient)
