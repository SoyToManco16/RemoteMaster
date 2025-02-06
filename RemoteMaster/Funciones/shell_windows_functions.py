import subprocess
import pyautogui
import time
from Funciones.system_funcions import get_os
from colorama import Fore

# Prevenir errores en sistemas Unix a la hora de usar RemoteMaster
current_os = get_os()
if current_os == "Windows":
    import winrm

def remote_desktop_with_password(hostname, username, password):
    """ Función para iniciar sesión en RDP con mstsc y contraseña automatizada """
    
    # Llamar al comando mstsc para abrir la ventana de RDP
    subprocess.Popen(["mstsc", "/v:" + hostname])  # Abre mstsc con la IP proporcionada
    
    # Esperar unos segundos para que la ventana RDP se abra
    time.sleep(2)
    
    # Escribir el nombre de usuario
    pyautogui.write(username)
    pyautogui.press('tab')  # Moverse al campo de la contraseña
    

    # Escribir la contraseña
    pyautogui.write(password)
    
    # Presionar 'Enter' para intentar iniciar sesión
    pyautogui.press('enter')

    print("Conexión RDP iniciada.")

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

def start_winrm_interactive_session(session):
    print("1 momento")
    


