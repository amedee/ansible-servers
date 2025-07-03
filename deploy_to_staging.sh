#!/bin/bash

# Generate the current date and time in the format YYYY-MM-DD_HH-MM-SS
timestamp="$(date +'%Y-%m-%d_%H-%M-%S')"

vagrant up --provision --provider=virtualbox 2>&1 | tee "logs/vagrant_$timestamp.log"
ansible-galaxy install -r requirements.yml

# Run ansible-playbook and pipe the output to tee with the generated filename
ansible-playbook playbooks/site.yml \
	-i inventory/staging \
	--vault-password-file ~/.vault_pass.txt \
	-v 2>&1 | tee "logs/ansible-playbook_$timestamp.log"
