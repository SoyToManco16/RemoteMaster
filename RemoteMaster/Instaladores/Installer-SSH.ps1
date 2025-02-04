# Instalar el servidor OpenSSH
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Iniciar el servicio SSH y configurarlo para que se inicie automáticamente
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'

# Añadir las reglas de firewall para el puerto SSH
if (-not (Get-NetFirewallRule -Name "SSHD-In-TCP")) {
    New-NetFirewallRule -Name "SSHD-In-TCP" -DisplayName "OpenSSH Server (sshd) Inbound" -Description "Permitir tráfico SSH entrante" -Profile Any -Direction Inbound -Action Allow -Protocol TCP -LocalPort 22
}

if (-not (Get-NetFirewallRule -Name "SSHD-Out-TCP")) {
    New-NetFirewallRule -Name "SSHD-Out-TCP" -DisplayName "OpenSSH Server (sshd) Outbound" -Description "Permitir tráfico SSH saliente" -Profile Any -Direction Outbound -Action Allow -Protocol TCP -LocalPort 22
}

Write-Host "OpenSSH Server instalado y configurado exitosamente."
