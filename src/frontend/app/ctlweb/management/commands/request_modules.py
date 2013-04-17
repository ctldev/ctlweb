#vim: set fileencoding=utf-8

from django.core.management.base import BaseCommand
from ctlweb.views import request_modules

class Command(BaseCommand):
    option_list = BaseCommand.option_list + ()

    help = u"""Mit diesem Kommando werden alle neuen Komponenten aus den
    Clustern angefragt."""

    def handle(self, *args, **options):
        request_modules()
