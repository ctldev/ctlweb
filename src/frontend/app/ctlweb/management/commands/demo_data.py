#vim: set fileencoding=utf-8

from django.core.management.base import BaseCommand
from ctlweb.models import *
from django.contrib.auth.models import Group, Permission, User
import datetime

class Command(BaseCommand):
    option_list = BaseCommand.option_list + ()

    help = u"""Mit diesem Kommando kann eine Demo-Instanz erzeugt werden"""

    def handle(self, *args, **options):
        self.import_cluster()
        self.import_interfaces()
        self.import_user()
        self.import_user_rights()
        self.import_components()
        self.import_connections()

    def import_cluster(self):
        self.cl1 = Cluster( hostname="https://www.c1.de", \
                            username="foobaa",\
                            port=22)
        self.cl2 = Cluster( hostname="https://www.c2.de", \
                            username="foobaa",\
                            port=22)
        self.cl3 = Cluster( hostname="https://www.c3.de", \
                            username="foobaa", \
                            port=22)

        self.cl1.save()
        self.cl2.save()
        self.cl3.save()

    def import_interfaces(self):
        self.i1 = Interfaces(name="Matrizen", ci_hash="01",
                ci="Quellcode I1")
        self.i2 = Interfaces(name="Grundlagen", ci_hash="02",
                ci="Quellcode I2")
        self.i3 = Interfaces(name="Addition", ci_hash="03",
                ci="aaaaaaaaaa aaaaaaaaaa aaaaaaaaaa aaaaaaaaaa aaaaaaaaaa aaaaaaaaaa aaaaaaaaaa aaaa" \
                +"\n alle meine entchen schwimmen auf dem See")
        
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
        self.user4 = User(username="superuser",
                first_name="a",
                last_name="b",
                email="abc@def.de",
                is_staff=True,
                is_active=True,
                is_superuser=True,
                last_login=today,
                date_joined=today)

        self.user1.set_password('teamprojekt')
        self.user2.set_password('teamprojekt')
        self.user3.set_password('teamprojekt')
        self.user4.set_password('teamprojekt')

        self.user1.save()
        self.user2.save()
        self.user3.save()
        self.user4.save()

    def import_user_rights(self):
        pass
#        permissions = Permission.objects
#        permissions.get(codename="can_see_description").user_set.add(self.user1)
#        permissions.get(codename="can_see_description").user_set.add(self.user2)
#        permissions.get(codename="can_see_homecluster").user_set.add(self.user1)
#        permissions.get(codename="can_see_key").user_set.add(self.user1)
#        permissions.get(codename="can_see_path").user_set.add(self.user1)
#        permissions.get(codename="can_see_code").user_set.add(self.user1)
#        permissions.get(codename="can_see_code").user_set.add(self.user2)
#        permissions.get(codename="can_set_active").user_set.add(self.user1)
#        permissions.get(codename="add_group").user_set.add(self.user1)
#        permissions.get(codename="change_user").user_set.add(self.user1)
#        permissions.get(codename="change_group").user_set.add(self.user1)
#    
    def import_components(self):
        self.co1 = Components(exe_hash="foo",
                description="Diese Komponente berechnet die LU-Zerlegung "+\
                    "mittels Gauß-Algorithmus",
                version="1.001.0001")
        self.co2 = Components(exe_hash="bar",
                description="DieseDiese Komponente addiert zwei MatrizenDiese Komponente addiert zwei MatrizenDiese Komponente addiert zwei Matrizen Komponente addiert zwei Matrizen",
                version="10001a")
        self.co3 = Components(exe_hash="foobar",
                description="Diese Komponente addiert zwei Zahlen miteinander.",
                version="10000000001")
        self.co4 = Components(exe_hash="barfoo",
                description="Diese Komponente addiert zwei komplexe Zahlen",
                version="10001.a")

        self.co1.save()
        self.co2.save()
        self.co3.save()
        self.co4.save()

        self.co1.set_active(self.user4)
        self.co2.set_active(self.user4)
        self.co3.set_active(self.user4)
        self.co4.set_active(self.user4)

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

        self.hc1 = Components_Cluster(cluster=self.cl1,
                component=self.co1,
                name="LU-Zerlegung")
        self.hc2 = Components_Cluster(cluster=self.cl2,
                component=self.co1,
                name="Gauß-LU-Zerlegung")
        self.hc3 = Components_Cluster(cluster=self.cl3,
                component=self.co1,
                name="LU-Zerlegung")
        self.hc4 = Components_Cluster(cluster=self.cl3,
                component=self.co2,
                name="Matrixaddition")
        self.hc5 = Components_Cluster(cluster=self.cl1,
                component=self.co3,
                name="Addition")
        self.hc6 = Components_Cluster(cluster=self.cl3,
                component=self.co3,
                name="einfache Addition")
        self.hc7 = Components_Cluster(cluster=self.cl1,
                component=self.co4,
                name="KomplexAddition")

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
