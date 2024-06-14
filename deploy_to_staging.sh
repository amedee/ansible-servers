#!/bin/bash
vagrant up --provision
ansible-playbook playbooks/site.yml -i inventory/staging/hosts.yml --vault-password-file ~/.vault_pass.txt
