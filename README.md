# Simplyblock Ansible
A small playbook to deploy an ansible cluster.

Create an inventory, e.g.:
```
[management_node]
192.168.10.121

[storage_nodes]
192.168.10.122
192.168.10.123
192.168.10.124
192.168.10.125 secondary=True
```

Run the playbook:
```
ansible-playbook -i hosts -e 'management_nic=ens18 data_nic=ens16 pool=pool1' cluster.yml
```
The optional variables `sbcli_package` and `sb_image` allow to specify a specific `sbcli` version to install, and an image that is used instead of the configured one.

You can use the `ssh.yml` playbook to accept any host keys from all hosts in your inventory and deploy your SSH public key:

```
ansible-playbook -i hosts -k -e "public_key='<key>'" ssh.yml
```
