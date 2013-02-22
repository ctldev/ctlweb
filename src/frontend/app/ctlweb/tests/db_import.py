# vim set fileencoding=utf-8

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from ctlweb.models import *
import datetime

def dbimport():
    #Webserver
    w1 = Webserver( name="Web1", 
                    domain="www.web1.de")
    w2 = Webserver( name="Web2", 
                    domain="www.web2.com")
    w3 = Webserver( name="Web3", 
                    domain="www.web3.en")
    w1.save()
    w2.save()
    w3.save()
    
    #Cluster
    cl1 = Cluster(domain="https://www.c1.de")
    cl2 = Cluster(domain="https://www.c2.de")
    cl3 = Cluster(domain="https://www.c3.de")
    cl1.save()
    cl2.save()
    cl3.save()

    #Interfaces
    i1 = Interfaces(
            name="Matrizen", 
            description="etliche Matrizenrechnungen",
            key="01")
    i2 = Interfaces(
            name="Grundlagen", 
            description="Addition, Subtraktion, Multiplikation und Division"+\
                        "von natürlichen Zahlen",
            key="02")
    i3 = Interfaces(
            name="Addition", 
            description="verschiedene Additionsverfahren",
            key="03")

    #User
    user1 = User(username="user1", 
                 first_name="foo",
                 last_name="bah",
                 email="foo@bah.de",
                 is_staff=False,
                 is_active=True,
                 is_superuser=False,
                 last_login=datetime.datetime.today(),
                 date_joined=datetime.datetime.today())
    user1.set_password('teamprojekt')
    user1.save()
    
    user2 = User(username="user2",
                 first_name="bah",
                 last_name="foo",
                 email="bah@foo.de",
                 is_staff=False,
                 is_active=True,
                 is_superuser=False,
                 last_login=datetime.datetime.today(),
                 date_joined=datetime.datetime.today())
    user2.set_password('teamprojekt')
    user2.save()

    user3 = User(username="inactiv",
                 first_name="abc",
                 last_name="xyz",
                 email="abc@xyz.de",
                 is_staff=False,
                 is_active=False,
                 is_superuser=False,
                 last_login=datetime.datetime.today(),
                 date_joined=datetime.datetime.today())
    user3.set_password('teamprojekt')
    user3.save()

    #TODO User + Rights
    Permission.objects.get(codename="can_see_description").user_set.add(user1)
    Permission.objects.get(codename="can_see_description").user_set.add(user2)
    Permission.objects.get(codename="can_see_homecluster").user_set.add(user1)
    Permission.objects.get(codename="can_see_homeserver").user_set.add(user1)
    Permission.objects.get(codename="can_see_key").user_set.add(user1)
    Permission.objects.get(codename="can_see_path").user_set.add(user1)
    Permission.objects.get(codename="can_see_code").user_set.add(user1)
    Permission.objects.get(codename="can_see_code").user_set.add(user2)


    #Components
    #TODO verbindung zu CLuster überarbeiten
    #TODO Programmer
    co1 = Components(
            name="LU-Zerlegung", 
            brief_description="LU-Zerlegung nach Gauß",
            description="Diese Komponente berechnet die LU-Zerlegung mittels Gauß",
            version="1.001.0001")
    co1.save()
    co1.homeserver.add(w1)
    co1.homeserver.add(w3)
    hc1 = Components_Cluster(cluster=cl1,
                            component=co1,
                            path="C:\Cluter\Cl1",
                            code="Implementierungscode von Co1 aif Cl1")
    hc1.save()
    co1.homecluster.add(cluster=cl1, path="C:\Cluster\Cl1", code="Implementierungscode für co1 auf Cluster1")
    co1.homecluster.add(cluster=cl2, path="C:\Cluster\Cl2", code="Implementierungscode für co1 auf Cluster2")
    co1.homecluster.add(cluster=cl3, path="C:\Cluster\Cl3", code="Implementierungscode für co1 auf Cluster3")
    co1.interfaces.add(i1)
    co1.programmer.add(email="foo@bah.de")
    co1.programmer.add(email="blabla@bla.de")

    co2 = Components(
            name="Matrix-Addition",
            brief_description="Addition von zwei Matrizen",
            description="Diese Komponente addiert zwei Matrizen",
            version="10001a")
    co2.save()
    co2.homeserver.add(w2)
    co2.homecluster.add(cluster=cl1, path="C:\Cluster\Cl1", code="Implementierungscode für co2 auf Cluster1")
    co2.homecluster.add(cluster=cl2, path="C:\Cluster\Cl2", code="Implementierungscode für co2 auf Cluster2")
    co2.homecluster.add(cluster=cl3, path="C:\Cluster\Cl3", code="Implementierungscode für co2 auf Cluster3")
    co2.interfaces.add(i1)
    co2.programmer.add(email="blubble@blub.org")

    co3 = Components(
            name="Addition",
            brief_description="Addiert zwei Zahlen",
            description="Diese Komponente addiert zwei Zahlen miteinander.",
            version="1000000000001")
    co3.save()
    co3.homeserver.add(w1)
    co3.homecluster.add(cluster=cl1, path="C:\Cluster\Cl1", code="Implementierungscode für co3 auf Cluster1")
    co3.homecluster.add(cluster=cl2, path="C:\Cluster\Cl2", code="Implementierungscode für co3 auf Cluster2")
    co3.homecluster.add(cluster=cl3, path="C:\Cluster\Cl3", code="Implementierungscode für co3 auf Cluster3")
    co3.interfaces.add(i2)
    co3.programmer.add(email="bah@foo.de")

    co4 = Components(
            name="komplexe Zahlen",
            brief_description="Addiert zwei komplexe Zahlen",
            description="Diese Komponente addiert zwei komplexe Zahlen",
            version="10001.a")
    co4.save()
    co4.homserver.add(w1)
    co4.homecluster.add(cluster=cl1, path="C:\Cluster\Cl1", code="Implementierungscode für co4 auf Cluster1")
    co4.homecluster.add(cluster=cl2, path="C:\Cluster\Cl2", code="Implementierungscode für co4 auf Cluster2")
    co4.homecluster.add(cluster=cl3, path="C:\Cluster\Cl3", code="Implementierungscode für co4 auf Cluster3")
    co4.interfaces.add(i3)
    co4.programmer.add(email="bah@foo.de")
    co4.programmer.add(email="abc@xyz.de")

