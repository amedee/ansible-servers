#!/bin/bash
vagrant up --provision --provider=virtualbox
ansible-galaxy install -r requirements.yml
ansible-playbook playbooks/site.yml -i inventory/staging/hosts.yml --vault-password-file ~/.vault_pass.txt -v
