import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_easyrsa_bin(host):
    easyrsa = host.file("/usr/share/easy-rsa/3/easyrsa")
    assert easyrsa.exists


def test_easyrsa_pki_dh(host):
    dh = host.file("/home/easyrsa/easyrsa/pki/dh.pem")
    assert dh.exists


def test_easyrsa_pki_server_request(host):
    easyrsa = host.file("/home/easyrsa/easyrsa/pki/reqs/server.req")
    assert easyrsa.exists


def test_openvpn_is_installed(host):
    package = host.package("openvpn")
    assert package.is_installed
