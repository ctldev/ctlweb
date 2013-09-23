#vim: set fileencoding=utf-8

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Befehl zur Erstellung eines individuellen Impressums. Es werden auf der
    Kommandozeile einige Daten abgefragt. Dabei sind einige optional und können
    leer sein, während andere angegeben werden müssen. Diese werden solange
    abgefragt bis etwas eingegeben wurde."""

    option_list = BaseCommand.option_list + ()
    def handle(self, *args, **options):
#Deklarierung der Variablen, die auf Leere überpüft werden und deswegen einen
#leeren String brauchen.
        org_name = org_street = org_city = admin_name = ""
#Angaben die nicht leer sein dürfen werden mit while Schleifen darauf geprüft,
#sodass sie so lange abgefragt werden bis sie nicht leer sind.
        while (org_name==""):
            print "Geben Sie bitte die Daten Ihrer Betreiberfirma/Betreiberorganisation an: "
#Verwendung von raw_input zur Vermeidung von Kompatibiltätsproblemen
            org_name = raw_input("Eingabe: ")
        print "Geben Sie bitte eine Unterabteilung ein, falls zutreffend."
        org_part = raw_input("Eingabe: ")
        while (org_street==""):
            print "Geben Sie bitte die Straße und Hausnummer ihrer Organisation/Firma an."
            org_street = raw_input("Eingabe: ")
        while (org_city==""):
            print "Geben Sie bitte die Postleitzahl und Stadt ihrer Organisation/Firma an."
            org_city = raw_input("Eingabe: ")
        print "Geben Sie bitte die Telefonnummer ihrer Organisation/Firma an."
        org_tel = raw_input("Eingabe: ")
        print "Geben Sie bitte die Faxnummer ihrer Organisation/Firma an."
        org_fax = raw_input("Eingabe: ")
        print "Geben Sie bitte den vollständigen Namen eines Betreuers Ihrer Seite ein."
        while (admin_name==""):
            admin_name = raw_input("Eingabe: ")
        print "Geben Sie bitte die Telefonnummer des Betreuers an."
        admin_tel = raw_input("Eingabe: ")
        print "Geben Sie bitte die E-Mail Addresse des Betreuers an."
        admin_mail = raw_input("Eingabe: ")
#Start der Generierung des HTML-Codes des Impressum
        impressum_string = \
            "<p><h4>Betreiber</p></h4> \n" \
            + org_name + "</br> \n"
#Optionale Angaben werden ignoriert wenn dazugehörige Variable leerer String.
        if (org_part != ""):
            impressum_string = impressum_string + org_part + "</br> \n"
        impressum_string = impressum_string \
            + org_street + "</br> \n" + org_city + "</br> \n" \
            + "Tel.: " + org_tel + "</br> \n" + "Fax: " + org_fax + \
            "</br> </p> \n \n"  + "<p><h4>Zuständiger Bearbeiter</h4> \n" \
            + admin_name + "</br> \n" + admin_tel + "</br> \n" + admin_mail \
            + "</p> <br/> <br/> \
            <p><strong>Haftung für Inhalte</strong></p> \
            Die Inhalte unserer Seiten wurden mit größter Sorgfalt erstellt. \
            Für die Richtigkeit, Vollständigkeit und Aktualität der Inhalte \
            können wir jedoch keine Gewähr übernehmen. Als Diensteanbieter sind wir gemäß § 7 Abs.1 TMG für \
            eigene Inhalte auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich. \
            Nach §§ 8 bis 10 TMG sind wir als Diensteanbieter jedoch nicht \
            verpflichtet, übermittelte oder gespeicherte fremde Informationen zu \
            überwachen oder nach Umständen zu forschen, die auf eine rechtswidrige \
            Tätigkeit hinweisen. Verpflichtungen zur Entfernung oder Sperrung der \
            Nutzung von Informationen nach den allgemeinen Gesetzen bleiben hiervon \
            unberührt. Eine diesbezügliche Haftung ist jedoch erst ab dem \
            Zeitpunkt der Kenntnis einer konkreten Rechtsverletzung möglich. Bei \
            Bekanntwerden von entsprechenden Rechtsverletzungen werden wir diese Inhalte \
            umgehend entfernen. \
            <p><strong>Haftung für Links</strong></p> \
            Unser Angebot enthält Links zu externen Webseiten Dritter, auf deren \
            Inhalte wir keinen Einfluss haben. Deshalb können wir für diese \
            fremden Inhalte auch keine Gewähr übernehmen. Für die Inhalte \
            der verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber der \
            Seiten verantwortlich. Die verlinkten Seiten wurden zum Zeitpunkt der Verlinkung \
            auf mögliche Rechtsverstöße überprüft. Rechtswidrige \
            Inhalte waren zum Zeitpunkt der Verlinkung nicht erkennbar. Eine permanente \
            inhaltliche Kontrolle der verlinkten Seiten ist jedoch ohne konkrete Anhaltspunkte \
            einer Rechtsverletzung nicht zumutbar. Bei Bekanntwerden von Rechtsverletzungen \
            werden wir derartige Links umgehend entfernen.\
            <p><strong>Urheberrecht</strong></p>\
            Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten \
            unterliegen dem deutschen Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung und \
            jede Art der Verwertung außerhalb der Grenzen des Urheberrechtes bedürfen \
            der schriftlichen Zustimmung des jeweiligen Autors bzw. Erstellers. Downloads \
            und Kopien dieser Seite sind nur für den privaten, nicht kommerziellen \
            Gebrauch gestattet. Soweit die Inhalte auf dieser Seite nicht vom Betreiber erstellt wurden, \
            werden die Urheberrechte Dritter beachtet. Insbesondere werden Inhalte Dritter als solche \
            gekennzeichnet. Sollten Sie trotzdem auf eine Urheberrechtsverletzung aufmerksam werden, bitten wir um einen entsprechenden Hinweis. \
            Bei Bekanntwerden von Rechtsverletzungen werden wir derartige Inhalte umgehend entfernen.\
            <p><strong>Datenschutz</strong></p>\
            Die Nutzung unserer Webseite ist in der Regel ohne Angabe personenbezogener Daten möglich. \
            Soweit auf unseren Seiten personenbezogene Daten (beispielsweise Name, Anschrift oder eMail-Adressen) \
            erhoben werden, erfolgt dies, soweit möglich, stets auf freiwilliger Basis. Diese Daten werden ohne Ihre \
            ausdrückliche Zustimmung nicht an Dritte weitergegeben. <br/>  \
            Wir weisen darauf hin, dass die Datenübertragung im Internet (z.B. \
            bei der Kommunikation per E-Mail) Sicherheitslücken aufweisen kann. \
            Ein lückenloser Schutz der Daten vor dem Zugriff durch Dritte ist nicht \
            möglich.<br/>\
            Der Nutzung von im Rahmen der Impressumspflicht veröffentlichten Kontaktdaten \
            durch Dritte zur Übersendung von nicht ausdrücklich angeforderter \
            Werbung und Informationsmaterialien wird hiermit ausdrücklich widersprochen. \
            Die Betreiber der Seiten behalten sich ausdrücklich rechtliche Schritte \
            im Falle der unverlangten Zusendung von Werbeinformationen, etwa durch Spam-Mails, \
            vor.<br />"
#Schreiben des String der den HTML-Code enthält.
        impressum_file = open("./template/impressum_personal.html","w")
        impressum_file.write(impressum_string)
        impressum_file.close()
