# Librerías del sistema
from Funciones.system_funcions import clear, get_os

# Librerias para paramiko
from Funciones.paramiko_functions import key_or_not, start_ssh

# Librerías funciones de red
from Funciones.network_functions import get_interfaces, get_neighbors, get_network_from_interface, show_ips_and_interfaces

# Librerías de personalización
from colorama import Fore

# Librería para los menús
from Menus.menus_rm import main_menu, show_menu_os_type, file_transfer_menu, shell_windows


# Ejecución del programa principal
if __name__ == "__main__":

    # Mostrar menu
    main_menu()

    # Preguntar al usuario si sabe ya el sistema operativo y la IP del host
    direct_connection = input(f"{Fore.CYAN}¿Ya sabes la IP y el sistema operativo del host al que deseas conectarte?, si solo conoces la IP introduce 'IP' (s/n): {Fore.RESET}").lower()

    if direct_connection == 's':
        # Si el usuario ya sabe la IP y el sistema operativo, saltar a la sección de selección del host y sistema operativo.
        choosehost = input(f"{Fore.CYAN}Introduce la dirección IP del host al que quiere conectarse: {Fore.RESET}")
        remote_os_type = input(f"{Fore.CYAN}Introduce el tipo de sistema operativo del host (Windows / Linux): {Fore.RESET}").strip().lower()

    elif direct_connection == 'ip':
        choosehost = input(f"{Fore.CYAN}Introduce la dirección IP del host al que quiere conectarse: {Fore.RESET}")
        remote_os_type = 'ip'
        
    elif direct_connection == 'n':
        """
        Si el usuario no conoce el host ni el sistema operativo de este
        muestra las interfaces de red del usuario
        """
        # Obtener redes
        interfaces_info = get_interfaces()
        show_ips_and_interfaces(interfaces_info)
        print(" ")

        """
        Con la dirección IP del usuario llama a la funcion get_network_from_interface
        que se encarga de calcular la red a la que pertenece la IP para poder pasarsela 
        a la funcion get_neighbors para obtener los hosts de la misma red en el caso de que estuviesen presentes
        """

        # Pedir dirección IP de la interfaz al usuario
        chosenet = input(f"{Fore.CYAN}Introduce la dirección IP de la interfaz que vas a utilizar: {Fore.RESET}")

        # Obtener la red de la direccion IP del usuario 
        user_network = get_network_from_interface(chosenet, interfaces_info)
        user_network = str(user_network) # Convertimos a string porque la función de nmap espera un string y no  <class 'ipaddress.IPv4Network'>
        print(" ")

        # Obtener equipos conectados de la red del usuario
        net_hosts = get_neighbors(user_network); print(" ")

        """
        Ahora pedimos la IP
        """

        # Introducir la IP a la que nos queremos conectar (Esta variable la pasamos a las funciones de paramiko)
        choosehost = input(f"{Fore.CYAN}Seleccione la dirección IP del host al que quiere conectarse: {Fore.RESET}")

        # Obtener el sistema operativo del host al que nos conectaremos
        remote_os_type = input(f"{Fore.CYAN}Introduce el tipo de sistema operativo del host (Windows / Linux): {Fore.RESET}").strip().lower()

    else:
        print(f"{Fore.RED}Opción no válida, saliendo de RemoteMaster... {Fore.RESET}")

    # Preguntar si el usuario tiene claves o va a iniciar con contraseña
    keyorpass = input(f"{Fore.CYAN}Si dispones de claves de acceso introduce s de lo contrario pulsa intro: {Fore.RESET}"); print(" ")

    # Capturar cliente ssh en una variable para poder manejarlo
    sshclient = key_or_not(choosehost, keyorpass)

    # Manejar errores a la hora de la creación del cliente ssh
    if sshclient == None:
        print(f"{Fore.RED}RemoteMaster no ha logrado conectarse a {choosehost}, saliendo del programa... {Fore.RESET}")
        exit()
    

    # Mostrar el menú según el sistema operativo del host
    clear()
    host_os_type = get_os()
    host_os_type = host_os_type.lower()
    show_menu_os_type(remote_os_type, host_os_type); print("")

    """
    host_os_type es el sistema operativo anfitrión
    remote_os_type es el sistema operativo remoto

    Si el SO nativo es Windows y el SO remoto es Windows muestra un menú con 3 opciones
    Si el SO nativo es Windows y el SO remoto es Linux muestra solo 2
    Si el SO nativo es Linux y el SO remoto es Linux muestra solo 2
    Si solo sabemos la IP del host remoto nos muestra un menú con dos opciones
    """

# Obtener la opción del usuario para elegir el tipo de conexión remota
answer = input("Introduce una opción: ").strip()

# Opción 1: Transferencia de archivos (SFTP) para todos los menús
if answer == "1":
    file_transfer_menu()

# Menú Windows a Windows (Opción 2: Shell Windows)
elif answer == "2" and remote_os_type == "windows" and host_os_type == "windows":
    shell_windows()  # Abre la shell de Windows

# Menú Linux a Linux (Opción 2: Shell SSH)
elif answer == "2" and remote_os_type == "linux" and host_os_type == "linux":
    start_ssh(sshclient)  # Abre la conexión SSH Linux a Linux

# Menú híbrido (Linux a Windows o Windows a Linux) (Opción 2: Shell SSH)
elif answer == "2" and (remote_os_type == "linux" and host_os_type == "windows") or (remote_os_type == "windows" and host_os_type == "linux"):
    start_ssh(sshclient)  # Abre la conexión SSH Híbrida

# Menú IPOnly (Opción 2: Shell SSH)
elif answer == "2" and (host_os_type == "windows" or host_os_type == "linux"):
    start_ssh(sshclient)  # Abre la conexión SSH con solo IP

# Menú Windows a Windows (Opción 3: Remote Desktop)
elif answer == "3" and remote_os_type == "windows" and host_os_type == "windows":
    remote_desktop()  # Abre la interfaz gráfica Remote Desktop

# Si la opción no es válida
else:
    print(f"{Fore.RED}Opción no válida, saliendo de RemoteMaster... {Fore.RESET}")

   


    


    


   