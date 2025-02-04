# Descargar el instalador de Nmap
$installerPath = "$env:TEMP\nmap-setup.exe"
Invoke-WebRequest -Uri "https://nmap.org/dist/nmap-7.91-setup.exe" -OutFile $installerPath

# Iniciar el instalador de Nmap
Start-Process -FilePath $installerPath -Wait

# Eliminar el instalador
Remove-Item $installerPath

# Agregar Nmap al PATH del sistema
$nmapPath = "C:\Program Files (x86)\Nmap"
if (-Not ($env:Path -contains $nmapPath)) {
    [System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";$nmapPath", [System.EnvironmentVariableTarget]::Machine)
}

# Verificar si Nmap se ha agregado correctamente al PATH
$updatedPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)
Write-Host "Nmap se ha instalado y agregado al PATH del sistema. Ruta actual del PATH:"
Write-Host $updatedPath