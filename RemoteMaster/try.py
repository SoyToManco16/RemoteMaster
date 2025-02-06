# Librerias
from colorama import Fore
import winrm

def exec_command_with_winrm(comando, protocol, hostname, username, password):
    
    """ Esta función recibe como parámetros el comando a ejecutar en winrm
     si queremos usar HTTP o HTTPs el host remoto su usuario y contraseña
     depende de el protocolo que usemos crea una sesión u otra """

    if protocol == "http":
        # Crea una sesión con HTTP
        session = winrm.Session(f'http://{hostname}:5985/wsman', 
                                auth=(username, password),
                                transport='ntlm')
        
    elif protocol == "https":
        # Crea una sesión con HTTPS
        session = winrm.Session(f'https://{hostname}:5986/wsman', 
                                auth=(username, password),
                                transport='ntlm', 
                                server_cert_validation='ignore') 
    else:
        print(f"{Fore.RED}Opción no válida, cerrando RemoteMaster...{Fore.RESET}")

    # Ejecutar comando
    result = session.run_cmd(comando)

    # Devolver resultado del comando y errores
    if result.status_code == 0:
        print(f"{Fore.CYAN}Salida del comando:{Fore.RESET} " + result.std_out.decode('latin-1'))
    else:
        print(f"{Fore.RED}Error al ejecutar el comando. Código de estado:{Fore.RESET} {result.status_code}")
        print(f"{Fore.RED}Salida del comando:{Fore.RESET} " + result.std_err.decode())

protocol = "https"
hostname = "192.168.1.15"
username = "Usuario"
password = "Micasa123"
comando = "ipconfig"
exec_command_with_winrm(comando, protocol, hostname, username, password)



