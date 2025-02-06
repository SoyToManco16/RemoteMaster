# Librerías del sistema
from Funciones.system_funcions import clear, get_os

# Librerias para paramiko
from Funciones.paramiko_functions import key_or_not, start_ssh, create_sftp_client

# Librerías para windows y powershell
from Funciones.shell_windows_functions import remote_desktop_with_password

# Librerías funciones de red
from Funciones.network_functions import get_interfaces, get_neighbors, get_network_from_interface, show_ips_and_interfaces

# Librerías de personalización
from colorama import Fore

# Librería para los menús
from Menus.menus_rm import main_menu, show_menu_os_type, file_transfer_menu, shell_windows


# Ejecución del programa principal
if __name__ == "__main__":

    # Obtener sistema nativo
    host_os = get_os()
    host_os = host_os.lower()

    # Mostrar menu
    clear()
    main_menu()

    try:

        # Preguntar al usuario si sabe ya el sistema operativo y la IP del host
        direct_connection = input(f"{Fore.CYAN}¿Ya sabes la IP y el sistema operativo del host al que deseas conectarte?. (s/n)\nSí quieres escanear tu red local introduce escanear: {Fore.RESET}").strip().lower()

        if direct_connection == 's':
            # Si el usuario ya sabe la IP y el sistema operativo, saltar a la sección de selección del host y sistema operativo.
            choosehost = input(f"{Fore.CYAN}Introduce la dirección IP del host al que quiere conectarse: {Fore.RESET}")
            remote_os = input(f"{Fore.CYAN}Introduce el tipo de sistema operativo del host (Windows / Linux): {Fore.RESET}").strip().lower()

        elif direct_connection == 'n':
            choosehost = input(f"{Fore.CYAN}Introduce la dirección IP del host al que quiere conectarse: {Fore.RESET}")
            remote_os = 'ip'
        
        elif direct_connection == 'escanear':
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

            # Introducir la IP a la que nos queremos conectar (Esta variable la pasamos a las funciones de paramiko)
            choosehost = input(f"{Fore.CYAN}Seleccione la dirección IP del host al que quiere conectarse: {Fore.RESET}")

            # Obtener el sistema operativo del host al que nos conectaremos
            remote_os = input(f"{Fore.CYAN}Introduce el tipo de sistema operativo del host (Windows / Linux): {Fore.RESET}").strip().lower()

        else:
            print(f"{Fore.RED}Opción no válida, saliendo de RemoteMaster... {Fore.RESET}")
            exit()

        # Preguntar si el usuario tiene claves o va a iniciar con contraseña
        keyorpass = input(f"{Fore.CYAN}Si dispones de claves de acceso introduce s de lo contrario pulsa intro: {Fore.RESET}"); print(" ")

        # Capturar cliente ssh en una variable para poder manejarlo
        sshclient, username, password = key_or_not(choosehost, keyorpass)

        # Manejar errores a la hora de la creación del cliente ssh
        if sshclient == None:
            print(f"{Fore.RED}RemoteMaster no ha logrado conectarse a {choosehost}, saliendo del programa... {Fore.RESET}")
            exit()

        # Mostrar el menú según el sistema operativo del host
        clear()
        show_menu_os_type(remote_os, host_os); print("")

        # Opciones de los menús
        def menu_utilidades(opcion, remote_os, host_os):
            match (opcion, remote_os, host_os):
        
                # Caso para transferencia de archivos
                case ("1", _, _):
                    if remote_os in ["windows", "linux", "ip"] and host_os in ["windows", "linux"]:
                        sftp_client = create_sftp_client(sshclient)

                        if sftp_client is None:
                            print(f"{Fore.RED}RemoteMaster no ha logrado crear una instancia SFTP, saliendo del programa... {Fore.RESET}")
                            exit()

                        file_transfer_menu(sshclient, sftp_client)
                    else:
                        print(f"{Fore.YELLOW}Combinación de sistemas no soportada para transferencia de archivos.{Fore.RESET}")

                # Caso para acceso remoto (Windows Shell o SSH según corresponda)
                case ("2", _, _):
                    if remote_os == "windows" and host_os == "windows":
                        shell_windows(sshclient, choosehost, username, password)
                    elif remote_os in ["windows", "linux", "ip"] and host_os in ["windows", "linux"]:
                        start_ssh(sshclient, choosehost, username)
                    else:
                        print(f"{Fore.YELLOW}Combinación de sistemas no soportada para acceso remoto.{Fore.RESET}")

                # Caso específico para escritorio remoto (solo Windows ↔ Windows)
                case ("3", "windows", "windows"):
                    remote_desktop_with_password(choosehost, username, password)

                # Caso por defecto si la opción no es válida
                case _:
                    print(f"{Fore.YELLOW}Opción no válida o combinación de sistemas no soportada.{Fore.RESET}")


        # Obtener opción del usuario y ejecutar la función
        opcion = input("Introduce una opción: ")
        menu_utilidades(opcion, remote_os, host_os)

    except KeyboardInterrupt:
        print(f"{Fore.LIGHTBLACK_EX}RemoteMaster cerrado...{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.YELLOW}Error inesperado: {e}")
    


    


   