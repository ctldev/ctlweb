#vim: set fileencoding=utf-8

import paramiko
import hashlib
import time
import datetime
import os
import zipfile
from ConfigParser import SafeConfigParser
from ctlweb.models import Cluster
from ctlweb.models import Components
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

def request_modules(testing=False):
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
            command = "ctl-getcomponent -a " + \
                    "-u %s -k %s -t %s" % (url, c.key, date)
        else:
            command = "ctl-getcomponent -a " + \
                    "-u %s -k %s" % (url, c.key)
        ssh.connect(c.domain, pkey=sshkey, port=c.port)
        if not testing:
            stdin, stdout, stderr = ssh.exec_command(command)
#if no error TODO needed?
        ModuleTokenValidation.create_token(url_token, c)
        ssh.close()


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
    try:
        token_db = ModuleTokenValidation.objects.get(token=token)
    except ModuleTokenValidation.DoesNotExist:
        return False
    return token_db.is_valid(cluster)

def receive_modules(request, token):
    cluster_ip = _get_client_ip(request)
    if not valid_token(token, cluster_ip):
        raise Http404
    cluster = Cluster.objects.get(ip=cluster)
    comp_form = ComponentRequestForm(request.POST or None, request.FILES or None)
    interface_form = InterfaceRequestForm(request.POST or None)
    file_success = False
    interface_success = False
    if interface_form.is_valid():
        clean_data = interface_form.cleaned_data
        name = clean_data["name"]
        description = clean_data["description"]
        key = clean_data["hash"]
        interface = Interface(name=name, description=description, key=key)
        interface.save()
        interface_success = True
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
    if not zipfile.is_zipfile(filename):
        return False
    with zipfile.ZipFile(filename, "r") as myzip:
        settings_file = myzip.open("control")
        parser = SafeConfigParser()
        parser.read(settings_file)
#TODO read settings
        if cluster.domain is not None:
            if cluster.domain == parser.get("DEFAULT", "host"):
                return False
        doc_file = myzip.open("doc.txt")
        desc = doc_file.read()
        doc_file.close()
        ci_file = myzip.open(parser.get("DEFAULT", "ci"))
        ci = ci_file.read()
        ci_file.close()
        domain = settings.SITE_DOMAIN
        localhost, created = Webserver.objects.get_or_create(domain=domain)
        exe_name = parser.get("DEFAULT", "name")
        exe_hash = parser.get("DEFAULT", "exe_hash")
        component = Components(name=exe_name, homeserver=localhost,
                homecluster=cluster, brief_description=desc, description=ci,
                is_active=True, version=version)
        component.save()
        interface, created = Interfaces.objects.get_or_create(key=exe_hash)
        interface.save()
        interface.components.add(component)
        interface.save()
        # TODO Programmierer gegebenfalls mit einbauen
        return True
