#!/bin/bash
# This script downloads all of the needed utilities for the CMMC project and
# installs them. This script needs to be run as root because there are commands
# that need elevated privileges.  This is to be added to the Ansible setup for
# each workstation.
# The '$1' is the parameter passed into the bash script.
# USAGE: sudo bash initScript.sh <username> <password>


apt update;
apt full-upgrade -y;
useradd -md /home/$1 -s /bin/bash -U $1;
usermod -aG users $1;
echo "$1:$2" | chpasswd;
apt install -y git-all ansible;
git clone https://github.com/kdn5436/CMMC-Compliance-Project.git;
ansible-playbook -c local -i 127.0.0.1, -l 127.0.0.1 CMMC-Compliance-Project/src/stiglevel2/ubuntu2004-stig.yml;
rm -rf CMMC-Compliance-Project;
apt remove -y git-all ansible;
apt autoremove;
systemctl reboot;
