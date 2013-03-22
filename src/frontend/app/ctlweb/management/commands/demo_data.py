#vim: set fileencoding=utf-8

from django.core.management.base import BaseCommand
from ctlweb.models import *
from django.contrib.auth.models import Group, Permission, User
import datetime

class Command(BaseCommand):
    option_list = BaseCommand.option_list + ()

    help = u"""Mit diesem Kommando kann eine Demo-Instanz erzeugt werden"""

    def handle(self, *args, **options):
        self.import_webserver()
        self.import_cluster()
        self.import_interfaces()
        self.import_user()
        self.import_user_rights()
        self.import_components()
        self.import_connections()

    def import_webserver(self):
        self.w1 = Webserver(name="Web1", domain="http://www.web1.de")
        self.w2 = Webserver(name="Web2", domain="https://www.web2.com")
        self.w3 = Webserver(name="Web3", domain="http://www.web3.en")

        self.w1.save()
        self.w2.save()
        self.w3.save()

    def import_cluster(self):
        self.cl1 = Cluster(domain="https://www.c1.de")
        self.cl2 = Cluster(domain="https://www.c2.de")
        self.cl3 = Cluster(domain="https://www.c3.de")

        self.cl1.save()
        self.cl2.save()
        self.cl3.save()

    def import_interfaces(self):
        self.i1 = Interfaces(name="Matrizen", key="01",
                description="etliche Matrizenrechnungen")
        self.i2 = Interfaces(name="Grundlagen", key="02",
                description="Addition, Subtraktion, Multiplikation und Division"+\
                    "von natürlichen Zahlen")
        self.i3 = Interfaces(name="Addition", key="03",
                description="Verschiedene Additionsverfahren")
        
        self.i1.save()
        self.i2.save()
        self.i3.save()

    def import_user(self):
        today = datetime.datetime.today()
        self.user1 = User(username="user1", 
                first_name="foo", 
                last_name="bah",
                email="foo@bah.de", 
                is_staff=False, 
                is_active=True,
                is_superuser=False, 
                last_login=today,
                date_joined=today)
        self.user2 = User(username="user2",
                first_name="bah",
                last_name="foo",
                email="bah@foo.de",
                is_staff=False,
                is_active=True,
                is_superuser=False,
                last_login=today,
                date_joined=today)
        self.user3 = User(username="inactive",
                first_name="abc",
                last_name="xyz",
                email="abc@xyz.de",
                is_staff=False,
                is_active=False,
                is_superuser=False,
                last_login=today,
                date_joined=today)

        self.user1.set_password('teamprojekt')
        self.user2.set_password('teamprojekt')
        self.user3.set_password('teamprojekt')

        self.user1.save()
        self.user2.save()
        self.user3.save()

    def import_user_rights(self):
        permissions = Permission.objects
        permissions.get(codename="can_see_description").user_set.add(self.user1)
        permissions.get(codename="can_see_description").user_set.add(self.user2)
        permissions.get(codename="can_see_homecluster").user_set.add(self.user1)
        permissions.get(codename="can_see_homeserver").user_set.add(self.user1)
        permissions.get(codename="can_see_key").user_set.add(self.user1)
        permissions.get(codename="can_see_path").user_set.add(self.user1)
        permissions.get(codename="can_see_code").user_set.add(self.user1)
        permissions.get(codename="can_see_code").user_set.add(self.user2)
        permissions.get(codename="can_set_active").user_set.add(self.user1)
        permissions.get(codename="add_group").user_set.add(self.user1)
        permissions.get(codename="change_user").user_set.add(self.user1)
        permissions.get(codename="change_group").user_set.add(self.user1)
    def import_components(self):
        self.co1 = Components(name="LU-Zerlegung",
                brief_description="LU-Zerlegung nach Gauß",
                description="Diese Komponente berechnet die LU-Zerlegung "+\
                    "mittels Gauß-Algorithmus",
                version="1.001.0001")
        self.co2 = Components(name="Matrix-Addition",
                brief_description="Addition von zwei Matrizen",
                description="Diese Komponente addiert zwei Matrizen",
                version="10001a")
        self.co3 = Components(name="Addition",
                brief_description="Addiert zwei Zahlen",
                description="Diese Komponente addiert zwei Zahlen miteinander.",
                version="10000000001")
        self.co4 = Components(name="komplexe Zahlen",
                brief_description="Addiert zwei komplexe Zahlen",
                description="Diese Komponente addiert zwei komplexe Zahlen",
                version="10001.a")

        self.co1.save()
        self.co2.save()
        self.co3.save()
        self.co4.save()

    def import_connections(self):
        self.ic1 = Interfaces_Components(interface=self.i1,
                component=self.co1)
        self.ic2 = Interfaces_Components(interface=self.i1,
                component=self.co2)       
        self.ic3 = Interfaces_Components(interface=self.i2,
                component=self.co2)       
        self.ic4 = Interfaces_Components(interface=self.i2,
                component=self.co3)       
        self.ic5 = Interfaces_Components(interface=self.i3,
                component=self.co4)
        
        self.ic1.save()
        self.ic2.save()
        self.ic3.save()
        self.ic4.save()
        self.ic5.save()

        self.co1.homeserver.add(self.w1)
        self.co1.homeserver.add(self.w3)
        self.co2.homeserver.add(self.w2)
        self.co3.homeserver.add(self.w1)
        self.co4.homeserver.add(self.w1)

        self.hc1 = Components_Cluster(cluster=self.cl1,
                component=self.co1,
                path="/path/on/cl1",
                code="Implementierungscode von co1 auf cl1")
        self.hc2 = Components_Cluster(cluster=self.cl2,
                component=self.co1,
                path="/path/on/cl2",
                code="Implementierungscode von co1 auf cl2")
        self.hc3 = Components_Cluster(cluster=self.cl3,
                component=self.co1,
                path="/path/on/cl3",
                code="Implementierungscode von co1 auf cl3")
        self.hc4 = Components_Cluster(cluster=self.cl3,
                component=self.co2,
                path="/path/on/cl3",
                code="Implementierungscode von co2 auf cl3")
        self.hc5 = Components_Cluster(cluster=self.cl1,
                component=self.co3,
                path="/path/on/cl1",
                code="Implementierungscode von co3 auf cl1")
        self.hc6 = Components_Cluster(cluster=self.cl3,
                component=self.co3,
                path="/path/on/cl3",
                code="Implementierungscode von co3 auf cl3")
        self.hc7 = Components_Cluster(cluster=self.cl1,
                component=self.co4,
                path="/path/on/cl1",
                code="Implementierungscode von co4 auf cl1")

        self.hc1.save()
        self.hc2.save()
        self.hc3.save()
        self.hc4.save()
        self.hc5.save()
        self.hc6.save()
        self.hc7.save()

        self.p1 = Programmer(component=self.co1, email="foo@bah.de")
        self.p2 = Programmer(component=self.co1, email="blabla@bla.de")
        self.p3 = Programmer(component=self.co2, email="blubble@blub.org")
        self.p4 = Programmer(component=self.co3, email="bah@foo.de")
        self.p5 = Programmer(component=self.co4, email="bah@foo.de")
        self.p6 = Programmer(component=self.co4, email="abc@xyz.de")

        self.p1.save()
        self.p2.save()
        self.p3.save()
        self.p4.save()
        self.p5.save()
        self.p6.save()

        self.co1.set_active(self.user1)
        self.co2.set_active(self.user1)
        self.co3.set_active(self.user1)
        self.co4.set_active(self.user1)
