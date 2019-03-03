from __future__ import absolute_import
from __future__ import unicode_literals
import os
import pytest
import logging
import testinfra.utils.ansible_runner


logging.basicConfig(level=logging.DEBUG)
# DEFAULT_HOST = 'all'


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('servers')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


@pytest.mark.parametrize('my_packages', [
  'openjdk-8-jre',
  'kibana',
  'logstash',
  'nginx',
  'apache2-utils',
  'elasticsearch'
])
def test_package_installed(host, my_packages):
    package = host.package(my_packages)
    assert package.is_installed


@pytest.mark.parametrize('my_services', [
  'elasticsearch',
  'kibana',
  'logstash',
  'nginx'
])
def test_service_running(host, my_services):
    service = host.service(my_services)
    assert service.is_running
    assert service.is_enabled


def test_certificate(host):
    cert = host.file("/etc/pki/tls/cert/logstash-forwarder.crt")
    assert cert.contains("""-----BEGIN CERTIFICATE-----
MIIDkTCCAnmgAwIBAgIJAKaBfTdRha68MA0GCSqGSIb3DQEBCwUAMG0xCzAJBgNV
BAYTAlVTMQ4wDAYDVQQIDAVUZXhhczEUMBIGA1UEBwwLU2FuIEFudG9uaW8xGzAZ
BgNVBAoMEm1hc3Rlci5nYXJhZ2VkLm9yZzEbMBkGA1UEAwwSbWFzdGVyLmdhcmFn
ZWQub3JnMB4XDTE5MDIwNzAwNTc1OFoXDTI5MDIwNDAwNTc1OFowbTELMAkGA1UE
BhMCVVMxDjAMBgNVBAgMBVRleGFzMRQwEgYDVQQHDAtTYW4gQW50b25pbzEbMBkG
A1UECgwSbWFzdGVyLmdhcmFnZWQub3JnMRswGQYDVQQDDBJtYXN0ZXIuZ2FyYWdl
ZC5vcmcwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDTJpY4a5k8XG/C
lqFc+FTuqQIfISyxY8M4hd/HwvF/B8Vc6VUkGny3WEKp5at0rTKQabIwWH7h5lN6
Sa9gvrUxrLnPZL/f3BCtyA5F2S/yKX5jrU6Sucd/L4M4nNlAdYitWUwYrdG+zFAp   d
9Al9eXeoqM7+nNnvaphXlBEEFm79naYCYqJuUCQdzdQoVWXDYIjfk7JIvc2Q5rPH
mZe6di/PxCPvIrcU1s2g9F6lb5MC9imQJgg0XwgN6z8mmdVmcBoE2TMzh1sg/sls
vxK/Cgce7aGhiV+Qzii2WLx28mVeh4O5IDn6gioWWHqVyTyOw3HZDF8o4jS1cTf4
kd0ibvepAgMBAAGjNDAyMBEGCWCGSAGG+EIBAQQEAwIGQDAdBgNVHREEFjAUghJt
YXN0ZXIuZ2FyYWdlZC5vcmcwDQYJKoZIhvcNAQELBQADggEBALsO3v5xU6Jl4vwg
QxxDfBMkKpRzf8vmYlDYV+l5uCqQl2HCkmnMidiR1Y/KXttV7XKqs2m/Md7bCr0k
/yxBraovjC12+bG0m1CLtoq7kbdIP9cO6V8eA5TSkpha0rgQXU96glnu2zKz3mkn
6g7Lmk4G/+dPWRP3ap2l62u+YVTa11kriNTBvZj0N/OuE0McbLGmQlYYL02SYDFu
ugXbbfAzSI3+Oqi8fCrEnbzD1/zKQ4PNTRHjqZCqH5jFtzsRj+X30oyddvVMdNz+
Ky98H8lkGnfAca0qUDw0sM6538f0JqQX4XKr2bfV689P+FG3IKk2m6aje+CBJoAp
PSWF7CU=
-----END CERTIFICATE-----
    """)
    assert cert.user == "root"
    assert cert.group == "logstash"
    assert cert.mode == 0o640


def test_htpasswd(host):
    cert = host.file("/etc/nginx/htpasswd.users")
    assert cert.contains("admin:$apr1$DnmQ0Ugg$TL8eq2TrSNDC79gCMO5c21")
    assert cert.user == "www-data"
    assert cert.mode == 0o660
