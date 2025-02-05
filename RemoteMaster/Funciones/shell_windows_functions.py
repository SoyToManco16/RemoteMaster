import subprocess
import pyautogui
import time
from Funciones.system_funcions import get_os

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

def start_winrm_interactive_session(hostname, username, password):
    print("1 momento")
    
def exec_command_with_winrm(comando, hostname, username, password):
    print("1 momento")
