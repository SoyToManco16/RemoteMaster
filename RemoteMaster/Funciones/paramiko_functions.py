# Librerías
import paramiko
from colorama import init, Fore
import sys
import os
import select
import subprocess
from Funciones.system_funcions import get_os

# Iniciar init para sistemas NT
init()

""" Pequeño bloque para comprobar el sistema desde el que se está ejecutando RemoteMaster
a la hora de ejecutar ciertas funciones """

myhost = get_os()
myhost = myhost.lower()

if myhost == "windows":
    import msvcrt
else:
    import termios
    import tty

# Funciones
def create_ssh_client_pass(hostname, port, username, password):

    """ Función que con los parámetros pedidos en el flujo principal, genera un cliente
     ssh o instancia a partir de la clave del equipo remoto """

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
    """
    Función que genera un cliente SSH usando una clave privada.
    Si la clave tiene una frase de contraseña, la utiliza; si no, la deja como None.
    """

    try:
        # Crear cliente SSH
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Cargar la clave privada correctamente
        private_key = paramiko.RSAKey.from_private_key_file(key_file, password=key_passphrase)

        # Conectar al servidor
        ssh_client.connect(hostname, port=port, username=username, pkey=private_key)

        return ssh_client

    except paramiko.AuthenticationException:
        print("Error: Fallo en la autenticación SSH.")
    except paramiko.SSHException as e:
        print(f"Error SSH: {e}")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de clave '{key_file}'.")
    except Exception as e:
        print(f"Error inesperado: {e}")

    return None
    
def create_sftp_client(ssh_client):
    """ Función que crea un cliente sftp a partir de un cliente ssh"""
    try:
        sftp_client = ssh_client.open_sftp()
        
        return sftp_client
    
    except Exception as e:
        return None

def key_or_not(host, answer):

    """Esta función se encarga de escoger que función lanzar a la hora de generar un cliente
    ssh, toma como parámetros un imput en el lado del flujo principal a la vez de el host 
    que obtiene mediante otro input que se ejecuta al principio del flujo para crear este cliente"""

    try:
        print(f"\n{Fore.LIGHTYELLOW_EX}Toma de datos para creación de clientes SSH{Fore.RESET}")
        print(f"{Fore.LIGHTYELLOW_EX}IP del host remoto: {host}{Fore.RESET}")

        hostname = host
        port = int(input(f"{Fore.LIGHTWHITE_EX}Selecciona el puerto del servidor al que te conectarás (pred: 22): {Fore.RESET}") or "22")
        username = input(f"{Fore.LIGHTWHITE_EX}Introduce el nombre de usuario con el que te conectarás al servidor: {Fore.RESET}")
        password = input(f"{Fore.LIGHTWHITE_EX}Introduce la contraseña del usuario: {Fore.RESET}")
        
        if answer == "s":
            key_file = input(f"{Fore.LIGHTWHITE_EX}Introduce la ruta hacia el archivo de la clave: {Fore.RESET}")
            key_passphrase = input(f"{Fore.LIGHTWHITE_EX}Introduce la frase de paso de la clave privada (si no tiene, deja vacío): {Fore.RESET}") or None
            ssh_client = create_ssh_client_keys(hostname, port, username, key_file, key_passphrase)
            return ssh_client, username, password
        
        else:
            ssh_client = create_ssh_client_pass(hostname, port, username, password)
            return ssh_client, username, password
        
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTBLACK_EX}Saliendo de RemoteMaster...{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Fore.RESET}")

def start_ssh(ssh_client, hostname, username):
    """Establece una sesión SSH interactiva.  
    - En Windows se abre una nueva terminal (CMD o PowerShell) que ejecuta el comando SSH.  
    - En Linux/macOS se usa la shell interactiva a través de Paramiko.
    """
    
    if ssh_client is None:
        print(f"{Fore.RED}No existe un cliente SSH, saliendo del programa... {Fore.RESET}")
        exit()

    try:
        if sys.platform.startswith("win"):
            # --- Opción para Windows: Abrir una nueva ventana de terminal con el comando SSH ---
            comando = f'start cmd /k "ssh {username}@{hostname}"'

            subprocess.Popen(comando, shell=True)
            print(f"{Fore.GREEN}Se ha abierto una nueva terminal para la sesión SSH.{Fore.RESET}")
            
        else:
            # --- Opción para Linux/macOS: Usar la sesión interactiva de Paramiko ---
            # Asignamos un pseudo-terminal (PTY) para interactividad
            shell = ssh_client.invoke_shell(term='xterm')
            print(f"{Fore.GREEN}Sesión SSH interactiva establecida{Fore.RESET}")

            # Guardar los ajustes de la terminal local para restaurarlos luego
            old_tty_settings = termios.tcgetattr(sys.stdin)
            try:
                tty.setraw(sys.stdin.fileno())
                shell.settimeout(0.0)

                while True:
                    # Esperamos por datos de la shell o de la entrada local
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
        print(f"{Fore.LIGHTBLACK_EX}Saliendo de RemoteMaster...{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Fore.RESET}")

    finally:
        # Cerrar recursos
        if sys.platform.startswith("win"):
            # En Windows, si se usó el método de terminal externa, se cierra la conexión del cliente
            if ssh_client.get_transport() is not None:
                ssh_client.close()
        else:
            if 'shell' in locals() and shell:
                shell.close()
            if ssh_client.get_transport() is not None:
                ssh_client.close()

def open_sftp_shell(ssh_client):
    
    """ Pendiente de comentar """

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

    except KeyboardInterrupt:
        print(f"{Fore.LIGHTBLACK_EX}Saliendo de RemoteMaster...{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Fore.RESET}")
    finally:
        sftp_client.close()

def sftp_upload_file(sftp_client, local_file, remote_file):
    """Función para subir un archivo a un servidor SFTP."""
    try:
        # Si la ruta local no es absoluta, la resolvemos usando el directorio actual
        if not os.path.isabs(local_file):
            local_file = os.path.join(os.getcwd(), local_file)

        # Subir el archivo local al archivo remoto
        sftp_client.put(local_file, remote_file)
        print(f"Archivo {local_file} subido a {remote_file}")
    
    except Exception as e:
        print(f"Ocurrió un error al subir el archivo: {e}")

def sftp_download_file(sftp_client, remote_file, local_file):
    """Función para descargar un archivo desde un servidor SFTP."""
    try:
        # Si la ruta local no es absoluta, la resolvemos usando el directorio actual
        if not os.path.isabs(local_file):
            local_file = os.path.join(os.getcwd(), local_file)

        # Descargar el archivo remoto al archivo local
        sftp_client.get(remote_file, local_file)
        print(f"Archivo {remote_file} descargado a {local_file}")
    
    except Exception as e:
        print(f"Ocurrió un error al descargar el archivo: {e}")
