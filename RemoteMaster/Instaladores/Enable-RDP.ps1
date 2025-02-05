# Verifica si se está ejecutando como administrador
$currentUser = [Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()
if (-not $currentUser.IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Este script debe ejecutarse como Administrador." -ForegroundColor Red
    exit
}

Write-Host "🔹 Habilitando Escritorio Remoto..." -ForegroundColor Cyan

# 1️⃣ Habilitar RDP en el registro de Windows
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections" -Value 0
Write-Host "✅ RDP habilitado en el registro."

# 2️⃣ Permitir conexiones RDP en la configuración del sistema
(Get-WmiObject -Class Win32_TerminalServiceSetting -Namespace "root\CIMV2\TerminalServices").SetAllowTsConnections(1)
Write-Host "✅ Conexiones RDP permitidas."

# 3️⃣ Habilitar el servicio RDP
Set-Service -Name TermService -StartupType Automatic
Start-Service -Name TermService
Write-Host "✅ Servicio de RDP habilitado y iniciado."

# 4️⃣ Desactivar Network Level Authentication (NLA) (Opcional, permite conexiones desde versiones antiguas)
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" -Name "UserAuthentication" -Value 0
Write-Host "✅ Network Level Authentication deshabilitado."

# 5️⃣ Agregar la regla de Firewall para permitir RDP
Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
Write-Host "✅ Firewall configurado para permitir RDP."

# 6️⃣ Verificar si el puerto RDP (3389) está habilitado
$rdpPort = Get-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" -Name "PortNumber" | Select-Object -ExpandProperty PortNumber
if ($rdpPort -ne 3389) {
    Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" -Name "PortNumber" -Value 3389
    Write-Host "✅ Puerto RDP establecido en 3389."
} else {
    Write-Host "✅ Puerto RDP (3389) ya está configurado correctamente."
}

# 7️⃣ Reiniciar el servicio RDP para aplicar cambios
Restart-Service TermService -Force
Write-Host "✅ Servicio RDP reiniciado."

# 8️⃣ Mostrar estado final
Write-Host "🎉 RDP ha sido habilitado correctamente. Puedes conectarte con MSTSC." -ForegroundColor Green
