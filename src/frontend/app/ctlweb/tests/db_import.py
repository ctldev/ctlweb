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
    i1.save()
    i2 = Interfaces(
            name="Grundlagen", 
            description="Addition, Subtraktion, Multiplikation und Division"+\
                        "von natürlichen Zahlen",
            key="02")
    i2.save()
    i3 = Interfaces(
            name="Addition", 
            description="verschiedene Additionsverfahren",
            key="03")
    i3.save()

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
                            path="C:\Cluster\Cl1",
                            code="Implementierungscode von Co1 auf Cl1")
    hc1.save()
    hc2 = Components_Cluster(cluster=cl2,
                            component=co1,
                            path="C:\Cluster\Cl2",
                            code="Implementierungscode von Co1 auf Cl2")
    hc2.save()
    hc3 = Components_Cluster(cluster=cl3,
                            component=co1,
                            path="C:\Cluster\Cl3",
                            code="Implementierungscode von Co1 aúf Cl3")
    hc3.save()
    i1.components.add(co1)
    p1 = Programmer(component=co1, email="foo@bah.de")
    p1.save()
    p2 = Programmer(component=co1, email="blabla@bla.de")
    p2.save()

    co2 = Components(
            name="Matrix-Addition",
            brief_description="Addition von zwei Matrizen",
            description="Diese Komponente addiert zwei Matrizen",
            version="10001a")
    co2.save()
    co2.homeserver.add(w2)
    hc4 = Components_Cluster(cluster=cl3,
                            component=co2,
                            path="C:\Cluster\Cl3",
                            code="Implementierungscode von Co2 aúf Cl3")
    hc4.save()
    i1.components.add(co2)
    p3 = Programmer(component=co2, email="blubble@blub.org")
    p3.save()

    co3 = Components(
            name="Addition",
            brief_description="Addiert zwei Zahlen",
            description="Diese Komponente addiert zwei Zahlen miteinander.",
            version="1000000000001")
    co3.save()
    co3.homeserver.add(w1)
    hc5 = Components_Cluster(cluster=cl1,
                            component=co3,
                            path="C:\Cluster\Cl1",
                            code="Implementierungscode von Co3 aúf Cl1")
    hc5.save()
    hc6 = Components_Cluster(cluster=cl3,
                            component=co3,
                            path="C:\Cluster\Cl3",
                            code="Implementierungscode von Co3 aúf Cl3")
    hc6.save()
    i2.components.add(co3)
    p4 = Programmer(component=co3, email="bah@foo.de")
    p4.save()

    co4 = Components(
            name="komplexe Zahlen",
            brief_description="Addiert zwei komplexe Zahlen",
            description="Diese Komponente addiert zwei komplexe Zahlen",
            version="10001.a")
    co4.save()
    co4.homeserver.add(w1)
    hc7 = Components_Cluster(cluster=cl1,
                            component=co4,
                            path="C:\Cluster\Cl1",
                            code="Implementierungscode von Co4 aúf Cl1")
    hc7.save()
    i3.components.add(co4)
    p5 = Programmer(component=co4, email="bah@foo.de")
    p5.save()
    p6 = Programmer(component=co4, email="abc@xyz.de")
    p6.save()
