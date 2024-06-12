Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  config.vm.network "private_network", type: "dhcp"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end

  config.vm.provision "shell", inline: <<-SHELL
    # Determine the IP address of the Vagrant box
    IP=$(hostname -I | awk '{print $2}')

    # Determine the Ubuntu version
    UBUNTU_VERSION=$(lsb_release -cs)
    HOSTNAME="ubuntu_${UBUNTU_VERSION}"

    # Create the inventory file
    mkdir -p /vagrant/inventory/staging
    echo "all:" > /vagrant/inventory/staging/hosts.yml
    echo "  hosts:" >> /vagrant/inventory/staging/hosts.yml
    echo "    ${HOSTNAME}:" >> /vagrant/inventory/staging/hosts.yml
    echo "      ansible_host: $IP" >> /vagrant/inventory/staging/hosts.yml
    echo "      ansible_user: vagrant" >> /vagrant/inventory/staging/hosts.yml
    echo "      ansible_ssh_private_key_file: .vagrant/machines/default/virtualbox/private_key" >> /vagrant/inventory/staging/hosts.yml
    echo "  children:" >> /vagrant/inventory/staging/hosts.yml
    echo "    mailservers:" >> /vagrant/inventory/staging/hosts.yml
    echo "      hosts:" >> /vagrant/inventory/staging/hosts.yml
    echo "        ${HOSTNAME}:" >> /vagrant/inventory/staging/hosts.yml
    echo "    webservers:" >> /vagrant/inventory/staging/hosts.yml
    echo "      hosts:" >> /vagrant/inventory/staging/hosts.yml
    echo "        ${HOSTNAME}:" >> /vagrant/inventory/staging/hosts.yml
  SHELL

end
