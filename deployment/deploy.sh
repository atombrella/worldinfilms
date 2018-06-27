#!/bin/bash

PROJECT_ROOT=${PWD}/../

export PATH=${PATH}:${PROJECT_ROOT}/node_modules/.bin

npm install
gulp

# database.yml playbook not needed
ansible-playbook -i inventory ansible/base.yml --ask-vault-pass
ansible-playbook -i inventory ansible/play.yml --ask-vault-pass
