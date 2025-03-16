# -*- mode: ruby -*-
# vi: set ft=ruby :
# frozen_string_literal: true

Vagrant.configure(2) do |config|
  config.vm.box = 'boxen/ubuntu-24.04'
  config.vm.disk :disk, size: '20GB', primary: true
  config.vm.network 'private_network', type: 'dhcp'
  config.vm.network 'forwarded_port', guest: 80, host: 8080, host_ip: '127.0.0.1'
  config.vm.network 'forwarded_port', guest: 443, host: 8443, host_ip: '127.0.0.1'
  config.vm.provider 'virtualbox' do |vb|
    vb.memory = 2048
    vb.linked_clone = true
  end
  config.vm.provision 'shell', inline: <<-SHELL
    parted --fix --script /dev/sda resizepart 3 100%
    pvresize /dev/sda3
    lvresize -rl +100%FREE /dev/ubuntu-vg/ubuntu-lv
  SHELL
  script = 'inventory/staging/get_inventory.sh'
  config.vm.provision 'shell', path: script, run: 'always'
end
