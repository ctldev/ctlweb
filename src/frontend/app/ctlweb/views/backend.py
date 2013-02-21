#vim: set fileencoding=utf-8

import paramiko
import hashlib
import time
import datetime
import os
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

def valid_token(token):
#TODO
    return False

def receive_modules(request, token):
    if not valid_token(token):
        raise Http404
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
        file_success = import_manifest(filename)
        os.remove(filename)
    dict_response = dict()
    dict_response["component_success"] = file_success
    dict_response["interface_success"] = interface_success
    dict_repsonse["comp_form"] = comp_form
    dict_response["inter_form"] = interface_form
    context = RequestContext(request, dict_response)
    return render_to_response('receive_components.html', context_instance=context)
