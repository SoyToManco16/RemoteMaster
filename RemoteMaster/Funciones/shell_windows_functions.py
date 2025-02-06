import subprocess
import pyautogui
import time
import warnings
from Funciones.system_funcions import get_os
from colorama import init, Fore

# Inicializar init para colores en terminales NT
init()

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

    print(f"{Fore.GREEN}Conexión RDP iniciada.{Fore.RESET}")

def exec_command_with_winrm(comando, protocol, hostname, username, password):
    
    """ Esta función recibe como parámetros el comando a ejecutar en winrm
    si queremos usar HTTP o HTTPs el host remoto su usuario y contraseña
    depende de el protocolo que usemos crea una sesión u otra """

    # Suprimir warnings de la librería winrm
    warnings.filterwarnings("ignore", category=UserWarning, module='winrm')
    
    try:
        # Crear sesión basada en el protocolo
        if protocol == "http":
            session = winrm.Session(f'http://{hostname}:5985/wsman', 
                                    auth=(username, password),
                                    transport='ntlm')
            
        elif protocol == "https":
            session = winrm.Session(f'https://{hostname}:5986/wsman', 
                                    auth=(username, password),
                                    transport='ntlm', 
                                    server_cert_validation='ignore') 
        else:
            print(f"{Fore.RED}Opción no válida, cerrando RemoteMaster...{Fore.RESET}")
            return
        
        # Ejecutar comando PowerShell
        result = session.run_ps(comando)
        
        # Devolver resultado del comando y errores
        if result.status_code == 0:
            print(f"{Fore.CYAN}Salida del comando:{Fore.RESET} " + result.std_out.decode('latin-1'))
        else:
            print(f"{Fore.RED}Error al ejecutar el comando. Código de estado:{Fore.RESET} {result.status_code}")
            print(f"{Fore.RED}Salida del comando:{Fore.RESET} " + result.std_err.decode('latin-1'))

    except winrm.exceptions.WinRMTransportError as e:
        print(f"{Fore.RED}Error de transporte de WinRM: {e}{Fore.RESET}")
    except winrm.exceptions.InvalidCredentialsError as e:
        print(f"{Fore.RED}Credenciales inválidas: {e}{Fore.RESET}")
    except winrm.exceptions.WinRMClientError as e:
        print(f"{Fore.RED}Error en el cliente de WinRM: {e}{Fore.RESET}")
    except winrm.exceptions.InvalidWSManFaultError as e:
        print(f"{Fore.RED}Error en WSMan: {e}{Fore.RESET}")
    except winrm.exceptions.WinRMError as e:
        print(f"{Fore.RED}Error en WinRM: {e}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Error inesperado: {e}{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTBLACK_EX}Saliendo de RemoteMaster...{Fore.RESET}")
    
