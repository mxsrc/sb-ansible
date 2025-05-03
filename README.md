# Simplyblock Ansible
A small playbook to deploy an ansible cluster.

Create an inventory, e.g.:
```
[management_nodes]
192.168.10.111
192.168.10.115

[storage_nodes]
192.168.10.112 ssds="['0000:00:02.0', '0000:00:03.0', '0000:00:04.0', '0000:00:05.0']"
192.168.10.113 ssds="['0000:00:02.0', '0000:00:03.0', '0000:00:04.0', '0000:00:05.0']"
192.168.10.114 ssds="['0000:00:02.0', '0000:00:03.0', '0000:00:04.0', '0000:00:05.0']"
```

Run the playbook:
```
ansible-playbook -i hosts -e 'management_nic=eth0 data_nic=eth1 pool=pool1' cluster.yml
```
The optional variables `sbcli_package` and `sb_image` allow to specify a specific `sbcli` version to install, and an image that is used instead of the configured one.
Similarily, `ultra_image` will allow to specify a different ultra image to use.
The cluster can be set up with any number of management and storage nodes, and will be configured accordingly.
Parameters in `cluster_params` and `add_storage_node_params` will be used for cluster creation and adding storage nodes respectively.

You can use the `ssh.yml` playbook to accept any host keys from all hosts in your inventory and deploy your SSH public key:

```
ansible-playbook -i hosts -k -e "public_key='<key>'" ssh.yml
```

## Testing
The directory `test` includes scripts to test the API of a cluster.
Install the requirements and run the tests from the directory:

```
pytest --entrypoint=<IP> --cluster=<cluster_id> --secret=<secret>
```
