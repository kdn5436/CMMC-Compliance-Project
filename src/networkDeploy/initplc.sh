#!/bin/bash
# This script downloads all of the needed utilities for the CMMC project and
# installs them. It also goes the extra step to download the plc editor for
# Chinda's Chickens.  This script needs to be run as root because there are
# commands that need elevated privileges.  This is to be added to the Ansible
# setup for each workstation.


apt update;
apt full-upgrade -y;
apt install -y git-all ansible;
git clone https://github.com/kdn5436/CMMC-Compliance-Project.git;
ansible-playbook -c local -i 127.0.0.1, -l 127.0.0.1 CMMC-Compliance-Project/src/stiglevel2/ubuntu2004-stig.yml;
rm -rf CMMC-Compliance-Project;
apt remove -y git-all ansible;
adduser --home /home/<user> --shell /bin/bash <user>;
usermod -p ChangeMe123! <user>;
mkdir openplc;
cd openplc;
wget https://autonomylogic.com/wp-content/uploads/files/OpenPLC%20Editor%20for%20Linux.zip;
unzip OpenPLC\ Editor\ for\ Linux.zip;
cd OpenPLC_Editor/;
./install.sh;
cd ~/;
