# Para ejecutar este script se deben de seguir las siguientes recomendaciones
# 1 Tener instalador python 
# 2 Ejecutar como admnistrador
# Habilita RDP, WinRM, Crea certificado, NMAP, SSH 

# Chequea si el usuario es administrador del sistema
$currentUser = [Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()
if (-not $currentUser.IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Este script debe ejecutarse como Administrador." -ForegroundColor Red
    exit
}

function install_ssh(){

# Instalar el servidor OpenSSH
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Inciar servicio y habilitar para inicio automático
Start-Service -Name sshd
Set-Service -Name sshd -StartupType Automatic

# Crear reglas en el firewall para permitir conexiones
New-NetFirewallRule -Name "SSHD-In-TCP" -DisplayName "OpenSSH Server (sshd) Inbound" -Description "Permitir tráfico SSH entrante" -Profile Any -Direction Inbound -Action Allow -Protocol TCP -LocalPort 22
New-NetFirewallRule -Name "SSHD-Out-TCP" -DisplayName "OpenSSH Server (sshd) Outbound" -Description "Permitir tráfico SSH saliente" -Profile Any -Direction Outbound -Action Allow -Protocol TCP -LocalPort 22

if (-not (Get-NetFirewallRule -Name "SSHD-In-TCP")){
    Write-Host "No se ha creado la regla en el firewall, porfavor revise manualmente o vuelva a ejecutar el script" -ForegroundColor red
}

if (-not (Get-NetFirewallRule -Name "SSHD-Out-TCP")){
    Write-Host "No se ha creado la regla en el firewall, porfavor revise manualmente o vuelva a ejecutar el script" -ForegroundColor red
}

}

function enable_rdp(){

# Habilitar RDP en el registro de windows
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections" -Value 0

# Permitir conexiones RDP
(Get-WmiObject -Class Win32_TerminalServiceSetting -Namespace "root\CIMV2\TerminalServices").SetAllowTsConnections(1)

# Habilitar el servicio RDP
Set-Service -Name TermService -StartupType Automatic
Start-Service -Name TermService

# Agregar reglas a el firewall 

# Reglas para UDP
New-NetFirewallRule -Name "Remote Desktop (RDP)" -DisplayName "RDP Protocol UDP In" -Direction Inbound -Protocol UDP -LocalPort 3389 -Action Allow -Enabled True
New-NetFirewallRule -Name "Remote Desktop (RDP)" -DisplayName "RDP Protocol UDP Out" -Direction Outbound -Protocol UDP -LocalPort 3389 -Action Allow -Enabled True

# Reglas para TDP
New-NetFirewallRule -Name "Remote Desktop (RDP)" -DisplayName "RDP Protocol TCP In" -Direction Inbound -Protocol TCP -LocalPort 3389 -Action Allow -Enabled True
New-NetFirewallRule -Name "Remote Desktop (RDP)" -DisplayName "RDP Protocol TCP Out" -Direction Outbound -Protocol TCP -LocalPort 3389 -Action Allow -Enabled True

# Verificar si el puerto RDP está habilitado
$rdpPort = Get-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" -Name "PortNumber" | Select-Object -ExpandProperty PortNumber
if ($rdpPort -ne 3389) {
    Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" -Name "PortNumber" -Value 3389
    Write-Host "Puerto RDP establecido en 3389."
} else {
    Write-Host "Puerto RDP (3389) ya está configurado correctamente."
}

# Reiniciar servicio 
Restart-Service TermService -Force
Write-Host "RDP configurado correctamente !!" -ForegroundColor Green

}

function install_nmap(){

# Descargar nmap (Requiere una leve interfaz gráfica)
$installerPath = "$env:TEMP\nmap-setup.exe"
Invoke-WebRequest -Uri "https://nmap.org/dist/nmap-7.91-setup.exe" -OutFile $installerPath

# Iniciar instalador
Start-Process -FilePath $installerPath -Wait

# Agregar nmap a path
$nmapPath = "C:\Program Files (x86)\Nmap"
if (-Not ($env:Path -contains $nmapPath)) {
    [System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";$nmapPath", [System.EnvironmentVariableTarget]::Machine)
}

# Verificar si nmap está correctamente en PATH
$updatedPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)
Write-Host "Nmap se ha instalado y agregado al PATH del sistema." -ForegroundColor green

}

function create_cert(){

# Mostrar direcciones IP para crear certificado
$Interfaces = (Get-NetAdapter | Get-NetIPAddress) | Select-Object IPv4Address, InterfaceAlias | Format-Table
$Interfaces

$Interface_Name = Read-Host "Introduce la interfaz que vas a utilizar"
$HostIP = ((Get-NetAdapter | Get-NetIPAddress) | Select-Object IPv4Address, InterfaceAlias | Where-Object {$_.InterfaceAlias -eq $Interface_Name} ).IPv4Address

# Crear certificado autofirmado con información obtenida
# Obtener nombre del equipo
$hostname = $env:COMPUTERNAME

$server_cert = New-SelfSignedCertificate -DnsName $hostname, $HostIP -CertStoreLocation Cert:\LocalMachine\My

# ThumbPrint del certificado
$thumbprint = $server_cert.Thumbprint

if (Get-ChildItem -Path "Cert:\LocalMachine\My" | Where-Object Thumbprint -eq $thumbprint){
    Write-Host "Certificado generado correctamente"
} else {
    Write-Error "Ha ocurrido un error"
}

}

function enable_winrm(){

# Mostrar interfaces de red disponibles
$Interfaces = Get-NetIPAddress | Where-Object AddressFamily -eq 'IPv4' | Select-Object IPAddress, InterfaceAlias
$Interfaces | Format-Table -AutoSize

$interfaceAlias = Read-Host "Seleccione la interfaz (sin comillas)"

# Obtener el perfil de red y cambiar la categoría si es pública
$profile = Get-NetConnectionProfile | Where-Object { $_.InterfaceAlias -eq $interfaceAlias }

if ($profile -and $profile.NetworkCategory -eq "Public") {
    Set-NetConnectionProfile -InterfaceAlias $interfaceAlias -NetworkCategory Private
    Write-Host "✅ Perfil de red cambiado a Privado para la interfaz $interfaceAlias" -ForegroundColor Green
} else {
    Write-Host "⚠️ El perfil de red ya es Privado o no se requiere cambio." -ForegroundColor Yellow
}

# Intentar obtener reglas de firewall para WinRM
try {
    $winrmRules = Get-NetFirewallRule -DisplayGroup "Windows Remote Management" -ErrorAction Stop
    Write-Host "✅ Reglas de firewall para WinRM detectadas." -ForegroundColor Green
}
catch {
    Write-Host "⚠️ No se han detectado reglas predefinidas. Creando nuevas..." -ForegroundColor Yellow

    # Verificar si el error es porque no existen reglas
    if ($_.FullyQualifiedErrorId -eq "CmdletizationQuery_NotFound_DisplayGroup,Get-NetFirewallRule") {
        
        # Crear reglas automáticamente
        New-NetFirewallRule -DisplayName "WINRM HTTP" -Direction Inbound -Protocol TCP -LocalPort 5985 -Action Allow -Enabled True

        New-NetFirewallRule -DisplayName "WINRM HTTPS" -Direction Inbound -Protocol TCP -LocalPort 5986 -Action Allow -Enabled True
        
        # Verificación de creación
        $winrmRules = Get-NetFirewallRule | Where-Object DisplayName -like "*WinRM*"
        if (-not $winrmRules) {
            Write-Host "❌ No se pudieron crear las reglas. Contacte con un administrador." -ForegroundColor Red
            exit 1
        } else {
            Write-Host "Reglas de firewall creadas correctamente." -ForegroundColor Green
        }
    } else {
        Write-Host "❌ Error inesperado: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

# Iniciar y habilitar WinRM
Start-Service -Name WinRM
Set-Service -Name WinRM -StartupType Automatic
Enable-PSRemoting -Force

# Comprobar si se ha activado
Test-WSMan -ComputerName $env:COMPUTERNAME

}

function install_all(){
    install_nmap
    install_ssh
    create_cert
    enable_rdp
    enable_winrm
    install_python_dependencies
}

function install_python_dependencies(){
# Lista de librerías a instalar
pip install python-nmap
pip install psutil
pip install paramiko
pip install colorama
pip install pyautogui

}

function show_menu(){
    Write-Host "Instalador RemoteMaster para Windows (NT)" -ForegroundColor Cyan
    write-host "1. Instalar todas las dependencias y crear certificado"
    Write-Host "2. Instalar OpenSSH"
    Write-Host "3. Instalar nmap"
    Write-Host "4. Habilitar RDP (MSTSC)"
    Write-Host "5. Habilitar Winrm (Windows Remote Manager)"
    Write-Host "6. Crear certificado"
    Write-Host "7. Instalar solo librerías de python"
}

# Menú instalador
show_menu

$option = Read-Host "Introduce una opción (1 - 6)"

if ($option -eq "1"){
    install_all
} elseif ($option -eq "2") {
    install_ssh
} elseif ($option -eq "3") {
    install_nmap
} elseif ($option -eq "4") {
    enable_rdp
} elseif ($option -eq "5") {
    enable_winrm
} elseif ($option -eq "6") {
    create_cert
} elseif ($option -eq "7") {
    install_python_dependencies
} else {
    Write-Host "Eso no es una opción "
}

