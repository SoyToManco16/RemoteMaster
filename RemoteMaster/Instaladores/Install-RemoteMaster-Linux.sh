#!/bin/bash

# Ejecutar como administrador

if [ "$(id -u)" -eq 1 ]; then
    echo "Debes ejecutar el script como administrador"
    exit(1)

# Instalar OpenSSH server
apt update
apt install openssh-server

# Iniciar e habilitar
systemctl start sshd
systemctl enable sshd
