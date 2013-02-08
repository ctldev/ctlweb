#vim: set fileencoding=utf-8

import paramiko
import hashlib
import time
from ctlweb.models import Cluster
from ctlweb.models import Components
from ctlweb.models import ModuleTokenValidation
from django.db.models import Max
from django.db.models import Q
from django.conf import settings
from django.core.urlresolvers import reverse

class CTLMissingHostKeyPolicy(paramiko.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        q_query = (Q(ip__exact=hostname)|Q(domain__exact=hostname))
        query = Cluster.objects.filter(q_query)
        if query.exists():
            client._host_keys.add(hostname, key.get_name(), key)
            return
        raise SSHException('Unknown server %s' % hostname)

def _gen_sec_token(domain):
    secret = settings.SECRET_KEY
    hextime = '%08x' % time.time()
    token = hashlib.sha256(secret + domain + hextime).hexdigest()
    return token

def request_modules():
    ssh = paramiko.SSHClient()
    cluster = Cluster.objects.all()

    for c in cluster:
        sshkey = paramiko.PKey(data=c.key)
        ssh.set_missing_host_key_policy(CTLMissingHostKeyPolicy())
        domain = c.domain
        if domain is None:
            domain = "" + c.ip
        date = Components.objects.all().aggregate(Max('date_creation'))
        date = date['date_creation__max']
        url_token = _gen_sec_token(domain)
        url = reverse('component_receive', args=[url_token])
        if date is not None:
            command = "ctl-getmodules -a " + \
                    "-u %s -k %s -t %s" % (url, c.key, date)
        else:
            command = "ctl-getmodules -a " + \
                    "-u %s -k %s" % (url, c.key)
        ssh.connect(c.domain, pkey=sshkey, port=c.port)
        stdin, stdout, stderr = ssh.exec_command(command)
#if no error TODO needed?
        ModuleTokenValidation.create_token(url_token, c)
        ssh.close()

def receive_modules(request, token):
    return render_to_response('home.html',
            context_instance=RequestContext(request))
