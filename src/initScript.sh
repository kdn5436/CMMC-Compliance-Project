#!/bin/bash
# This script downloads all of the needed utilities for the CMMC project and
# installs them. This script needs to be run as root because there are commands
# that need elevated privileges.  This is to be added to the Ansible setup for
# each workstation.


apt update;
apt upgrade;
apt install git-all ansible;
git clone https://github.com/kdn5436/CMMC-Compliance-Project.git;
ansible-playbook -c local -i 127.0.0.1, -l 127.0.0.1 CMMC-Compliance-Project/src/lvl2/roles/ubuntu2004STIG/tasks/main.yml;
rm -r CMMC-Compliance-Project.git;
apt remove git-all ansible;
