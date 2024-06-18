#!/bin/bash

# Determine the IP address of the Vagrant box
IP=$(hostname -I | awk '{print $2}')

# Determine the Ubuntu version
UBUNTU_VERSION=$(lsb_release -cs)
HOSTNAME="ubuntu_${UBUNTU_VERSION}"

# Create the inventory file
INVENTORY="/vagrant/inventory/staging"
mkdir --parents "${INVENTORY}"
cat <<EOF > "${INVENTORY}/hosts.yml"
---
all:
  hosts:
    ${HOSTNAME}:
      ansible_host: $IP
      ansible_user: vagrant
      ansible_ssh_private_key_file: .vagrant/machines/default/virtualbox/private_key
      dbserver_wp_db_host: localhost
  children:
    mailservers:
      hosts:
        ${HOSTNAME}:
    dbservers:
      hosts:
        ${HOSTNAME}:
    webservers:
      hosts:
        ${HOSTNAME}:
EOF
