# Openstack-ansible setup instructions

- Install ansible (if openstack.cloud collection isn't included, install it separately with ansible-galaxy collection install openstack.cloud)
  - On Debian based GNU/Linux systems (such as ubuntu and Pop_OS!), also install the python3-openstacksdk and python3-openstackclient packages:
```
sudo apt install ansible python3-openstacksdk python3-openstackclient
```
- From openstack, download \<project-name\>-openrc.sh and clouds.yml (API Access $\rightarrow$ Download OpenStack RC File)
  - Save this to /etc/openstack/clouds.yml or ~/.config/openstack/clouds.yml
  - Edit the clouds.yml file to include your password

- In a terminal run:
```
source <project-name>-openrc.sh
```

- Run the command:
```
ansible-playbook <scriptname>.yml
```
