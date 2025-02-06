# Para ejecutar este script se deben de seguir las siguientes recomendaciones
# 1. Tener instalado Python.
# 2. Ejecutar como Administrador.

# Resumen del instalador:
# - Instala OpenSSH, RDP (mstsc), nmap para RemoteMaster.
# - Crea un certificado y configura WinRM tanto en HTTP como en HTTPS.
# - Instala las dependencias de RemoteMaster en Python.

# Chequea si el usuario es administrador del sistema
$currentUser = [Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()
if (-not $currentUser.IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Este script debe ejecutarse como Administrador." -ForegroundColor Red
    exit
}

function select_network_interface {
    # Obtener interfaces de red activas con IPv4 (excluyendo loopback y APIPA)
    $interfaces = Get-NetIPAddress | Where-Object { 
        $_.AddressFamily -eq "IPv4" -and 
        $_.InterfaceIndex -gt 0 -and 
        $_.IPAddress -notlike "127.*" -and 
        $_.IPAddress -notlike "169.254.*" 
    } | Select-Object InterfaceAlias, IPAddress

    if (-not $interfaces) {
        Write-Error "No se encontraron interfaces de red válidas."
        exit 1
    }

    # Mostrar las interfaces disponibles
    Write-Host "Selecciona una interfaz de red para habilitar WinRM:" -ForegroundColor Cyan
    $i = 1
    foreach ($interface in $interfaces) {
        Write-Host "$i. [$($interface.InterfaceAlias)] - $($interface.IPAddress)"
        $i++
    }

    # Leer la selección del usuario
    $selection = Read-Host "Introduce el número de la interfaz (1 - $($interfaces.Count))"

    if ($selection -match "^\d+$" -and [int]$selection -ge 1 -and [int]$selection -le $interfaces.Count) {
        $selectedInterface = $interfaces[[int]$selection - 1]
        Write-Host "Seleccionaste: [$($selectedInterface.InterfaceAlias)] - $($selectedInterface.IPAddress)" -ForegroundColor Green
        return $selectedInterface.IPAddress
    } else {
        Write-Error "Selección inválida. Inténtalo de nuevo."
        exit 1
    }
}

$primaryIP = select_network_interface

function install_ssh {
    # Instalar el servidor OpenSSH
    Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

    # Iniciar servicio y habilitar para inicio automático
    Start-Service -Name sshd
    Set-Service -Name sshd -StartupType Automatic

    # Crear reglas en el firewall para permitir conexiones
    New-NetFirewallRule -Name "SSHD-In-TCP" -DisplayName "OpenSSH Server (sshd) Inbound" -Description "Permitir tráfico SSH entrante" -Profile Any -Direction Inbound -Action Allow -Protocol TCP -LocalPort 22
    New-NetFirewallRule -Name "SSHD-Out-TCP" -DisplayName "OpenSSH Server (sshd) Outbound" -Description "Permitir tráfico SSH saliente" -Profile Any -Direction Outbound -Action Allow -Protocol TCP -LocalPort 22

    if (-not (Get-NetFirewallRule -Name "SSHD-In-TCP")) {
        Write-Host "No se ha creado la regla en el firewall, por favor revise manualmente o vuelva a ejecutar el script" -ForegroundColor Red
    }

    if (-not (Get-NetFirewallRule -Name "SSHD-Out-TCP")) {
        Write-Host "No se ha creado la regla en el firewall, por favor revise manualmente o vuelva a ejecutar el script" -ForegroundColor Red
    }
}

function enable_rdp {
    # Habilitar RDP en el registro de Windows
    Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections" -Value 0

    # Permitir conexiones RDP
    (Get-WmiObject -Class Win32_TerminalServiceSetting -Namespace "root\CIMV2\TerminalServices").SetAllowTsConnections(1)

    # Habilitar el servicio RDP
    Set-Service -Name TermService -StartupType Automatic
    Start-Service -Name TermService

    # Agregar reglas al firewall para UDP y TCP
    New-NetFirewallRule -Name "RDP-UDP-In" -DisplayName "RDP Protocol UDP In" -Direction Inbound -Protocol UDP -LocalPort 3389 -Action Allow -Enabled True
    New-NetFirewallRule -Name "RDP-UDP-Out" -DisplayName "RDP Protocol UDP Out" -Direction Outbound -Protocol UDP -LocalPort 3389 -Action Allow -Enabled True
    New-NetFirewallRule -Name "RDP-TCP-In" -DisplayName "RDP Protocol TCP In" -Direction Inbound -Protocol TCP -LocalPort 3389 -Action Allow -Enabled True
    New-NetFirewallRule -Name "RDP-TCP-Out" -DisplayName "RDP Protocol TCP Out" -Direction Outbound -Protocol TCP -LocalPort 3389 -Action Allow -Enabled True

    # Verificar si el puerto RDP está habilitado
    $rdpPort = Get-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" -Name "PortNumber" | Select-Object -ExpandProperty PortNumber
    if ($rdpPort -ne 3389) {
        Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" -Name "PortNumber" -Value 3389
        Write-Host "Puerto RDP establecido en 3389."
    } else {
        Write-Host "Puerto RDP (3389) ya está configurado correctamente."
    }

    # Reiniciar el servicio RDP
    Restart-Service TermService -Force
    Write-Host "RDP configurado correctamente !!" -ForegroundColor Green
}

function install_nmap {
    # Descargar nmap (requiere una leve interfaz gráfica)
    $installerPath = "$env:TEMP\nmap-setup.exe"
    Invoke-WebRequest -Uri "https://nmap.org/dist/nmap-7.91-setup.exe" -OutFile $installerPath

    # Iniciar instalador y esperar a que finalice
    Start-Process -FilePath $installerPath -Wait

    # Agregar nmap a PATH (se asume instalación en "C:\Program Files (x86)\Nmap")
    $nmapPath = "C:\Program Files (x86)\Nmap"
    if (-Not ($env:Path -like "*$nmapPath*")) {
        [System.Environment]::SetEnvironmentVariable("Path", "$($env:Path);$nmapPath", [System.EnvironmentVariableTarget]::Machine)
    }

    Write-Host "Nmap se ha instalado y agregado al PATH del sistema." -ForegroundColor Green
}

function create_cert {
    
    $server_cert = New-SelfSignedCertificate `
        -DnsName $sanEntries `
        -CertStoreLocation Cert:\LocalMachine\My `
        -TextExtension "2.5.29.37={text}1.3.6.1.5.5.7.3.1" `
        -Subject "CN=$primaryIP"

    if (-not (Get-ChildItem -Path "Cert:\LocalMachine\My" | Where-Object { $_.Thumbprint -eq $server_cert.Thumbprint })) {
        Write-Error "Error al generar el certificado. Repita manualmente o use un certificado ya existente."
        exit 1
    }

    return [PSCustomObject]@{
        Certificate = $server_cert
        PrimaryIP   = $primaryIP
    }
}

function Import-CertificateToTrustedRoot($cert) {
    $rootStore = New-Object System.Security.Cryptography.X509Certificates.X509Store("Root", "LocalMachine")
    $rootStore.Open("ReadWrite")
    $rootStore.Add($cert)
    $rootStore.Close()
}

function enable_winrm_https {
    param (
        [Parameter(Mandatory=$true)]
        $cert,
        [Parameter(Mandatory=$true)]
        $primaryIP
    )

    # Esta función se ejecuta de forma silenciosa (solo muestra errores o el mensaje final de éxito)
    $ErrorActionPreference = "Stop"

    try {
        # Establecer las interfaces activas como privadas (sin salida)
        $interfaces = Get-NetAdapter | Where-Object { $_.Status -eq 'Up' }
        foreach ($interface in $interfaces) {
            $profile = Get-NetConnectionProfile | Where-Object { $_.InterfaceAlias -eq $interface.Name }
            if ($profile -and $profile.NetworkCategory -ne "Private") {
                Set-NetConnectionProfile -InterfaceAlias $interface.Name -NetworkCategory Private
            }
        }

        # Crear reglas de firewall para WinRM si no existen (sin salida)
        $winrmRules = Get-NetFirewallRule -DisplayGroup "Windows Remote Management" -ErrorAction SilentlyContinue
        if (-not $winrmRules) {
            New-NetFirewallRule -DisplayName "WINRM HTTP" -Direction Inbound -Protocol TCP -LocalPort 5985 -Action Allow -Enabled True | Out-Null
            New-NetFirewallRule -DisplayName "WINRM HTTPS" -Direction Inbound -Protocol TCP -LocalPort 5986 -Action Allow -Enabled True | Out-Null
        }

        # Configurar WinRM para HTTPS utilizando la IP principal
        $thumbprint = $cert.Thumbprint
        try {
            winrm delete winrm/config/Listener?Address=*+Transport=HTTPS 2>&1 | Out-Null
        } catch { }
        winrm create winrm/config/Listener?Address=*+Transport=HTTPS "@{Hostname=`"$primaryIP`";CertificateThumbprint=`"$thumbprint`"}" 2>&1 | Out-Null

        # Verificar que se haya creado el listener HTTPS
        $winrmConfig = winrm enumerate winrm/config/Listener
        if (-not ($winrmConfig | Select-String "Transport = HTTPS")) {
            throw "Error al activar WinRM en HTTPS."
        }

        # Iniciar y habilitar el servicio WinRM
        Start-Service -Name WinRM
        Set-Service -Name WinRM -StartupType Automatic
        Enable-PSRemoting -Force | Out-Null

        # Comprobar que WinRM funciona
        Test-WSMan -ComputerName $primaryIP -UseSSL | Out-Null

        # Mensaje final de éxito
        Write-Host "WinRM ha sido configurado correctamente en HTTPS." -ForegroundColor Green
    } catch {
        Write-Error $_.Exception.Message
    }
}

function install_python_dependencies {
    # Lista de librerías a instalar
    $librerias = @("python-nmap", "psutil", "paramiko", "pyautogui", "colorama", "pywinrm")

    foreach ($lib in $librerias) {
        try {
            python -m pip install $lib | Out-Null
        } catch {
            Write-Host "Error al instalar $lib" -ForegroundColor Red
        }
    }
    Write-Host "Todas las dependencias han sido cubiertas para el uso de RemoteMaster" -ForegroundColor Green
}


function install_all {
    install_nmap
    install_ssh

    # Crear certificado y configurar WinRM en HTTPS
    $certData    = create_cert
    Import-CertificateToTrustedRoot $certData.Certificate
    enable_rdp
    enable_winrm_https -cert $certData.Certificate -primaryIP $certData.PrimaryIP

    install_python_dependencies
}

function show_menu {
    Write-Host "Instalador RemoteMaster para Windows (NT)" -ForegroundColor Cyan
    Write-Host "1. Instalar todas las dependencias y crear certificado"
    Write-Host "2. Instalar OpenSSH"
    Write-Host "3. Instalar nmap"
    Write-Host "4. Habilitar RDP (MSTSC)"
    Write-Host "5. Habilitar WinRM (Windows Remote Manager)"
    Write-Host "6. Instalar solo librerías de Python"
}

# Menú instalador
show_menu
$option = Read-Host "Introduce una opción (1 - 6)"

switch ($option) {
    "1" {
        install_all
    }
    "2" {
        install_ssh
    }
    "3" {
        install_nmap
    }
    "4" {
        enable_rdp
    }
    "5" {
        # Para WinRM, se crea el certificado, se importa y se configura WinRM en HTTPS
        $certData = create_cert
        Import-CertificateToTrustedRoot $certData.Certificate
        enable_winrm_https -cert $certData.Certificate -primaryIP $certData.PrimaryIP
    }
    "6" {
        install_python_dependencies
    }
    default {
        Write-Host "Eso no es una opción" -ForegroundColor Red
    }
}
