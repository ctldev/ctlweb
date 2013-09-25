# vim: set fileencoding=utf-8

from django.test import TestCase
from django.utils.unittest import skipIf, skipUnless
from django.conf import settings
import paramiko
from os.path import expanduser, abspath, dirname
from ctlweb.models import Cluster
from ctlweb.models import Components
from ctlweb.models import Interfaces
from ctlweb.views.backend import request_modules, _import_manifest

class BackendTest(TestCase):
    use_ssh = False
    def setUp(self):
        hostname = "localhost"
        port = 22
        path = expanduser("~") + "/.ssh/"
        with open(path+"id_rsa.pub") as f:
            data = f.read()
        key = data
        ssh = paramiko.SSHClient()
        sshkey = paramiko.PKey(data=key)
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, pkey=sshkey, port=port)
            ssh.close()
        except:
           print "No local SSH-Connection allowed, skipping"
           use_ssh = False

        cluster = Cluster.objects.create(hostname=hostname, port=port, key=key)

    @skipIf(use_ssh, "ssh possible")
    @skipIf(True, "")
    def testBackendLocal(self):
        request_modules(ssh=False, pretend=True)

    @skipUnless(use_ssh, "ssh not possible")
    @skipIf(True, "")
    def testBackendSSH(self):
        request_modules(ssh=True, pretend=True)

    def testComponentParser(self):
        hostname = "localhost"
        cluster = Cluster.objects.get(hostname=hostname)
        filename = dirname(dirname(settings.DJANGO_ROOT)) + "/"
        filename += "usr/share/doc/ctlweb/example_package.tgz"
        success = _import_manifest(filename, cluster)
        self.failUnlessEqual(success, True)
        self.failUnless(Components.objects.all().values_list())
        self.failUnless(Interfaces.objects.all().values_list())
