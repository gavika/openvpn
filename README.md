gavika.openvpn
=========

Install and configure OpenVPN. Build and manage your own OpenVPN server.

Requirements
------------

The role should be used along with `gavika.easy_rsa`.

Role Variables
--------------

| Variable | Default Value | Description | Required? |
|----------|---------------|-----------|-------------|
| easy_rsa_local_pool_directory | /tmp/ca_openvpn_pool | The directory to use a temporary location to store certifacte requests, certificates, etc. | Yes |
| openvpn_client_users | [] | List of openvpn client usernames. It is recommended to use only alphanumeric characters. | No |
| openvpn_port | 1194 | The port on which OpenVPN server runs | Yes |
| openvpn_protocol | Default: udp Choices: tcp or udp | The network protocol to use | Yes |
| openvpn_server_ip_address | The IP address of the OpenVPN server | The value used in generated client certificates | Yes |
| openvpn_generated_configurations_local_pool | false. Boolean. | Whether to copy the generated client configurations to the local(The controller machine on which the ansible-playbook is executed.) pool directory. | Yes |
| openvpn_route_all_traffic | True. Boolean. | Route all internet traffic via the OpenVPN server | Yes |
| openvpn_use_opendns_public_dns | True. Boolean. | Push OpenDNS DNS servers to clients | Yes |
| openvpn_additional_configs | [] | Additional OpenVPN server configuration. List of dictionaries. Each list item is a pair of key, value. Example <br> openvpn_additional_configs: <br> - push: "topology subnet" <br> - push: "route 192.168.4.5 255.255.255.255" | Yes |
| openvpn_default_firewalld_zone | public | The zone name to use in Firewalld configuration. Relevant only for EL | Yes |


In order to build a CA server and an OpenVPN server using `gavika.easy_rsa` and
`gavika.openvpn`, you have to execute the roles a few times depending on your
needs. You are responsible to execute the roles the required number of times and
in required order. Examples are provided in documentation. Typically, you will
have to execute `open-vpn-playbook.yml` twice and `easy-rsa-playbook.yml` once.

Here's an example of executing the playbooks:
```sh
# openvpn: setup local pool directories, install openvpn, create server request,
# create client requests
ansible-playbook -i my-inventory.yml openvpn-playbook.yml
# easy_rsa: build the CA server, import and sign requests, fetch CA certificates
ansible-playbook -i my-inventory.yml easy-rsa-playbook.yml
# openvpn:  use signed requests, setup openvpn, generate client configurations
ansible-playbook -i my-inventory.yml openvpn-playbook.yml
```

Dependencies
------------
The `gavika.openvpn` role depends on `gavika.easy_rsa`.

The role `gavika.openvpn` should be used along with `gavika.easy_rsa`.

Example playbook to setup CA server: `easy-rsa-playbook.yml`
----------------
```yml
---
- hosts: ca_server
  become: true
  vars:
    easy_rsa_req_country: "IN"
    easy_rsa_req_province: "KA"
    easy_rsa_req_city: "Bangalore"
    easy_rsa_req_org: "Gavika"
    easy_rsa_req_email: "admin@gavika.com"
    easy_rsa_req_ou: "Gavika"
    easy_rsa_local_pool_directory: /tmp/ca_openvpn_pool # No trailing /
    easy_rsa_server_request_to_import: "server.req"
    easy_rsa_ca_server_mode: true
  roles:
    - role: gavika.easy_rsa
```

Example playbook to install the OpenVPN server: `openvpn-playbook.yml`

```yml
---
- hosts: openvpn_server
  become: true
  vars:
    openvpn_client_users:
      - janedoe
      - johndoe
    easy_rsa_req_country: "IN"
    easy_rsa_req_province: "KA"
    easy_rsa_req_city: "Bangalore"
    easy_rsa_req_org: "My Organization"
    easy_rsa_req_email: "admin@example.com"
    easy_rsa_req_ou: "My Organization Unit"
  roles:
    - role: gavika.easy_rsa
    - role: gavika.openvpn
```

Example inventory: `my-inventory`:
```yml
all:
  hosts:
    placeholder
  children:
    ca_server:
      hosts:
        dev-ca-01.example.com:
          ansible_become: true
          ansible_user: ubuntu
          ansible_host: 192.168.3.5
          easy_rsa_ca_server_mode: true
          ansible_python_interpreter: /usr/bin/python3
    openvpn_server:
      hosts:
        dev-vpn-01.example.com:
          ansible_python_interpreter: /usr/bin/python3
          ansible_become: true
          ansible_user: ubuntu
          ansible_host: 192.168.3.6
          openvpn_server_ip_address: 192.168.3.6
```

License
-------

Apache License, Version 2.0

Author Information
------------------
Sudheera Satyanarayana

Gavika
* https://www.gavika.com

* Blog: https://www.techchorus.net
* Twitter: https://www.twitter.com/bngsudheer
* Github: https://github.com/bngsudheer
