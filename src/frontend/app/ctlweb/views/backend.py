#vim: set fileencoding=utf-8

import paramiko
import hashlib
import time
import datetime
import os
import zipfile
import tarfile
import re
from ConfigParser import SafeConfigParser
from ctlweb.models import Cluster
from ctlweb.models import Components
from ctlweb.models import Components_Cluster
from ctlweb.models import Interfaces
from ctlweb.models import Interfaces_Components
from ctlweb.models import ModuleTokenValidation
from ctlweb.models import Programmer
from ctlweb.forms import ComponentRequestForm
from ctlweb.forms import ComponentDeleteForm
from django.db.models import Max
from django.db.models import Q
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

class CTLMissingHostKeyPolicy(paramiko.MissingHostKeyPolicy):
    """Accepting those Keys that are placed in the Database"""
    def missing_host_key(self, client, hostname, key):
        host = hostname
        m = re.match('\[(\S+)\]:\d+$', hostname)
        if m:
            host = m.group(1)
        q_query = (Q(ip__exact=host)|Q(domain__exact=host))
        query = Cluster.objects.filter(q_query)
        if query.exists():
            client._host_keys.add(hostname, key.get_name(), key)
            return
        raise paramiko.SSHException('Unknown server %s' % hostname)

def _gen_sec_token(domain):
    """generate a secure Token to not let everybody contribute fake Modules"""
    secret = settings.SECRET_KEY
    hextime = '%08x' % time.time()
    token = hashlib.sha256(secret + domain + hextime).hexdigest()
    return token

def send_user(user, cluster=None, ssh=True, pretend=False):
    if cluster is None:
        cluster = Cluster.objects.all()
    if not isinstance(cluster, list):
        cluster = [cluster,]
    for c in cluster:
        port = c.port
        if not c.port:
            port = 22
        ssh = paramiko.SSHClient()
        ssh_file = settings.SSH_KEY_FILE
        ssh_passwd = settings.SSH_KEY_PASSWORD
        ssh_user = c.username
        sshkey = paramiko.RSAKey.from_private_key_file(ssh_file, ssh_passwd)
        ssh.set_missing_host_key_policy(CTLMissingHostKeyPolicy())
        domain = c.ip
        if domain is None:
            domain = "" + c.domain
        if ssh:
            ssh.connect(hostname=domain, username=ssh_user, port=c.port,
                    key_filename=ssh_file, look_for_keys=False)
            shell = ssh.invoke_shell(term="vt220")
            response = ""
            if pretend:
                response += _send_message(shell, "s")
            response += _send_message(shell, "2")
            response += _send_message(shell, user.username)
            for key in user.userkey_set:
                response += send_message(shell, key.key)
            response += _send_message(shell, "q")
            print response
            ssh.close

def remove_user(user, cluster=None, ssh=True, pretend=False):
    if cluster is None:
        cluster = Cluster.objects.all()
    if not isinstance(cluster, list):
        cluster = [cluster,]
    for c in cluster:
        port = c.port
        if not c.port:
            port = 22
        ssh = paramiko.SSHClient()
        ssh_file = settings.SSH_KEY_FILE
        ssh_passwd = settings.SSH_KEY_PASSWORD
        ssh_user = c.username
        sshkey = paramiko.RSAKey.from_private_key_file(ssh_file, ssh_passwd)
        ssh.set_missing_host_key_policy(CTLMissingHostKeyPolicy())
        domain = c.ip
        if domain is None:
            domain = "" + c.domain
        if ssh:
            ssh.connect(hostname=domain, username=ssh_user, port=c.port,
                    key_filename=ssh_file, look_for_keys=False)
            shell = ssh.invoke_shell(term="vt220")
            response = ""
            if pretend:
                response += _send_message(shell, "s")
            response += _send_message(shell, "3")
            response += _send_message(shell, user.username)
            response += _send_message(shell, "q")
            print response
            ssh.close

def request_modules(ssh=True, pretend=False, request_all=False):
    """request all Modules of all Clusters of the Database"""
    ssh = paramiko.SSHClient()
    cluster = Cluster.objects.all()

    for c in cluster:
        port = c.port
        if not c.port:
            port = 22
        #paramiko-based commands
        ssh_file = settings.SSH_KEY_FILE
        ssh_passwd = settings.SSH_KEY_PASSWORD
        ssh_user = c.username
        sshkey = paramiko.RSAKey.from_private_key_file(ssh_file, ssh_passwd)
        ssh.set_missing_host_key_policy(CTLMissingHostKeyPolicy())
        domain = c.ip
        if domain is None:
            domain = "" + c.domain
        date = Components.objects.all().aggregate(Max('date_creation'))
        date = date['date_creation__max']
        # generate secure Token and append to url
        url_token = _gen_sec_token(domain)
        url = reverse('component_receive', args=[url_token])
        # use ssh for testing if enabled, ssh is also used normally
        if ssh:
            ssh.connect(hostname=domain, username=ssh_user, port=c.port,
                    key_filename=ssh_file, look_for_keys=False)
            shell = ssh.get_transport().open_session()
            cmd = "ctl-component push"
            if date and not request_all:
                cmd += " --timestamp %s" % date.date()
            cmd += " %s" % url
            if not pretend:
                shell.exec_command(cmd)
            ModuleTokenValidation.create_token(url_token, c)

PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', )

def _get_client_ip(request):
    """get the client ip from the request
    """
    remote_address = request.META.get('REMOTE_ADDR')
    # set the default value of the ip to be the REMOTE_ADDR if available
    # else None
    ip = remote_address
    # try to get the first non-proxy ip (not a private ip) from the
    # HTTP_X_FORWARDED_FOR
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        # remove the private ips from the beginning
        while (len(proxies) > 0 and proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
            # take the first ip which is not a private
            # one (of a proxy)
        if len(proxies) > 0:
            ip = proxies[0]
    return ip

def _valid_token(token):
    """test if a given token is valid for the given cluster"""
    try:
        token_db = ModuleTokenValidation.objects.get(token=token)
    except ModuleTokenValidation.DoesNotExist:
        return False
    return token_db.cluster, token_db.is_valid(token_db.cluster)

@csrf_exempt
def receive_modules(request, token):
    """handle incoming POST-request to receive modules"""
    cluster_ip = _get_client_ip(request)
    cluster, is_valid = _valid_token(token)
    if not is_valid:
#        raise Http404
        print "token is not valid, continueing nonetheless"
#    cluster = Cluster.objects.get(ip=cluster_ip)
    comp_form = ComponentRequestForm(request.POST or None, request.FILES or None)
    delete_form = ComponentDeleteForm(request.POST or None)
    file_success = False
    delete_success = False
    #handle component-delete-form
    if delete_form.is_valid():
        exe_hash = delete_form.cleaned_data['exe_hash']
        component = Components.objects.get(exe_hash=exe_hash)
        comp_cluster = Components_Cluster.objects.get(cluster=cluster,
                                                      component=component)
        comp_cluster.delete()
    #handle component-add-form
    if comp_form.is_valid():
        with request.FILES['manifest'] as manifest:
            file_success = _import_manifest(manifest, cluster)
    dict_response = dict()
    dict_response["component_success"] = file_success
    dict_response["delete_success"] = delete_success
    dict_response["comp_form"] = comp_form
    dict_response["delete_form"] = delete_form
    context = RequestContext(request, dict_response)
    return render_to_response('receive_components.html', context_instance=context)

def _import_manifest(filename, cluster):
    """handle the uploaded module-file, return True on succes, else False"""
    temp_path = '/tmp/'
    with tarfile.open(fileobj=filename, mode='r:gz') as myzip:
        control_file = myzip.extractfile("control")
        parser = SafeConfigParser()
        parser.readfp(control_file)
#        if cluster.domain is not None:
#            if cluster.domain == parser.get("DEFAULT", "host"):
#                return False
        doc_file = myzip.extractfile("description.txt")
        desc = doc_file.read()
        ci_name = parser.get('DEFAULT', 'ci')
        ci_file=myzip.extractfile(ci_name)
        ci = ci_file.read()
        ci_hash = _hash_file(myzip.extractfile(ci_name, 'rb'))
        domain = settings.SITE_DOMAIN
        name = parser.get("DEFAULT", "name")
        exe_hash = parser.get("DEFAULT", "exe_hash")
        path = parser.get('DEFAULT', 'exe')
        version = "1.0"
        if parser.has_option('DEFAULT', 'version'):
            version = parser.get("DEFAULT", "version")
        if Components.objects.filter(exe_hash=exe_hash):
            component = Components.objects.get(exe_hash=exe_hash)
            component.description = desc
            component.version = version
        else:
            component = Components(description=desc, is_active=False,
                                   version=version, exe_hash=exe_hash)
        component.save()
        comp_cluster = Components_Cluster(component=component,
                                          cluster=cluster, name=name)
        comp_cluster.save()
        from os.path import splitext, basename
        interface_name = splitext(basename(ci_name))[0]
        interface, created = Interfaces.objects.get_or_create(ci_hash=ci_hash)
        if created:
            interface.name = interface_name
            interface.ci = ci
        interface.save()
        inter_comp = Interfaces_Components(interface=interface,
                component=component)
        inter_comp.save()
        if parser.has_option('DEFAULT', 'author'):
            authors = parser.get('DEFAULT', 'author').split(' ')
            for author in authors:
                programmer = Programmer(component, author)
                programmer.save()
        return True
    return False

def _hash_file(file_object, hashtype=None, block_size=512):
    """ Generates a hash for a file-like object with given hashlib.<hashtype>,
    defaults to hashlib.md5()."""
    if not hashtype:
        import hashlib
        hashtype = hashlib.md5()
    for data in iter(lambda: f.read(block_size)):
        hashtype.update(data)
    import base64
    return base64.b64encode(hashtype.digest()).decode('utf8')
