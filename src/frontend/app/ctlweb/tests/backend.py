# vim: set fileencoding=utf-8

from django.test import TestCase
import paramiko
from os.path import expanduser
from ctlweb.models import Cluster
from ctlweb.views.backend import request_modules

class BackendTest(TestCase):
    def setUp(self):
        ip = "127.0.0.1"
        domain = "localhost"
        port = 22
        path = expanduser("~") + "/.ssh/"
        with open(path+"id_rsa.pub") as f:
            data = f.read()
        key = data
        ssh = paramiko.SSHClient()
        sshkey = paramiko.PKey(data=key)
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, pkey=sshkey, port=port)
            ssh.close()
        except:
            self.assertTrue(False, "local SSH-Server running?")
        cluster = Cluster.objects.create(ip=ip, domain=domain, port=port, key=key)

    def testBackendConnection(self):
        request_modules()
