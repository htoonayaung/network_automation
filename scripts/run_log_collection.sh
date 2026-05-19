#!/bin/bash

cd /home/ubuntu/network_automation
ansible-playbook -i inventory/inventory.yml playbooks/collect_logs.yml
