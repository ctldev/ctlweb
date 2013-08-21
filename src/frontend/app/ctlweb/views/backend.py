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
from ctlweb.forms import ComponentRequestForm
from ctlweb.forms import InterfaceRequestForm
from django.db.models import Max
from django.db.models import Q
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

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

def request_modules(ssh=True, pretend=False):
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
            print domain, ssh_file, ssh_user
            ssh.connect(hostname=domain, username=ssh_user, port=c.port,
                    key_filename=ssh_file, look_for_keys=False)
            shell = ssh.invoke_shell(term="vt220")
            response = ""
            if pretend:
                response += _send_message(shell, "s")
            response += _send_message(shell, "1")
            if date is None:
                response += _send_message(shell, "y")
            else:
                response += _send_message(shell, "n")
                response += _send_message(shell, "%s" % date.date())
            response += _send_message(shell, url)
            response += _send_message(shell, "q")
            print response
            #if no error TODO needed?
            ModuleTokenValidation.create_token(url_token, c)
            ssh.close()

def _send_message(shell, message, end='\n', wait=0.01):
    response = _receive_response(shell, wait)
    message = message + end
    shell.sendall(message)
    response += _receive_response(shell, wait)
    return response

def _receive_response(shell, wait=0.01):
    time.sleep(wait)
    response = ''
    while shell.recv_ready():
        response += response + shell.recv(10)
        time.sleep(wait)
    return response


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

def valid_token(token, cluster):
    """test if a given token is valid for the given cluster"""
    try:
        token_db = ModuleTokenValidation.objects.get(token=token)
    except ModuleTokenValidation.DoesNotExist:
        return False
    return token_db.is_valid(cluster)

def receive_modules(request, token):
    """handle incoming POST-request to receive modules"""
    cluster_ip = _get_client_ip(request)
    if not valid_token(token, cluster_ip):
        raise Http404
    cluster = Cluster.objects.get(ip=cluster)
    comp_form = ComponentRequestForm(request.POST or None, request.FILES or None)
    interface_form = InterfaceRequestForm(request.POST or None)
    file_success = False
    interface_success = False
    #handle interface-form
    if interface_form.is_valid():
        clean_data = interface_form.cleaned_data
        name = clean_data["name"]
        description = clean_data["description"]
        key = clean_data["hash"]
        interface = Interface(name=name, description=description, key=key)
        interface.save()
        interface_success = True
    #handle component-form
    if comp_form.is_valid():
        date = datetime.datetime.today()
        date = datetime.datetime.strftime(date, '%s')
        filename = settings.MEDIA_ROOT + date + '.tar.gz'
        destination = open(filename, 'wb+')
        for chunk in request.FILES['manifest'].chunks():
            destination.write(chunk)
        destination.close()
        file_success = _import_manifest(filename, cluster)
        os.remove(filename)
    dict_response = dict()
    dict_response["component_success"] = file_success
    dict_response["interface_success"] = interface_success
    dict_repsonse["comp_form"] = comp_form
    dict_response["inter_form"] = interface_form
    context = RequestContext(request, dict_response)
    return render_to_response('receive_components.html', context_instance=context)

def _import_manifest(filename, cluster):
    """handle the uploaded module-file, return True on succes, else False"""
    temp_path = '/tmp/'
    with tarfile.open(filename, 'r:gz') as myzip:
        settings_file = myzip.extract("control", temp_path)
        control_file = temp_path + 'control'
        parser = SafeConfigParser()
        parser.read(control_file)
        if cluster.domain is not None:
            if cluster.domain == parser.get("DEFAULT", "host"):
                return False
        doc_file = myzip.extractfile("doc.txt")
        desc = doc_file.read()
        doc_file.close()
        ci_name = parser.get('DEFAULT', 'ci')
        myzip.extract(ci_name, temp_path)
        ci_file = open(temp_path + ci_name)
        ci = ci_file.read()
        ci_file.close()
        domain = settings.SITE_DOMAIN
        exe_name = parser.get("DEFAULT", "name")
        exe_hash = parser.get("DEFAULT", "exe_hash")
        path = parser.get('DEFAULT', 'exe')
        version = "1.0"
        if parser.has_option('DEFAULT', 'version'):
            version = parser.get("DEFAULT", "version")
        component = Components(name=exe_name, brief_description=desc, 
                description=ci, is_active=True, version=version)
        component.save()
        comp_cluster = Components_Cluster(component=component,
                cluster=cluster, path=path, code=ci)
        comp_cluster.save()
        interface, created = Interfaces.objects.get_or_create(key=exe_hash)
        interface.save()
        inter_comp = Interfaces_Components(interface=interface,
                component=component)
        inter_comp.save()
        # TODO Programmierer gegebenfalls mit einbauen
        return True
    return False
