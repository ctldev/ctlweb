#vim: set fileencoding=utf-8

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    option_list = BaseCommand.option_list + ()
    def handle(self, *args, **options):
        self.get_input()

    def get_input(self):
        print "Geben Sie bitte die Daten Ihrer Betreiberfirma/Betreiberorganisation an: "
        org_name = raw_input("Eingabe: ")
        print "Geben Sie bitte eine Unterabteilung ein, falls zutreffend."
        org_part = raw_input("Eingabe: ")
        print "Geben Sie bitte die Straße und Hausnummer ihrer Organisation/Firma an."
        org_street = raw_input("Eingabe: ")
        print "Geben Sie bitte die Postleitzahl und Stadt ihrer Organisation/Firma an."
        org_city = raw_input("Eingabe: ")
        print "Geben Sie bitte die Telefonnummer ihrer Organisation/Firma an."
        org_tel = raw_input("Eingabe: ")
        print "Geben Sie bitte die Faxnummer ihrer Organisation/Firma an."
        org_fax = raw_input("Eingabe: ")
        print "Geben Sie bitte den vollständigen Namen eines Betreuers Ihrer Seite ein."
        admin_name = raw_input("Eingabe: ")
        print "Geben Sie bitte die Telefonnummer des Betreuers an."
        admin_tel = raw_input("Eingabe: ")
        print "Geben Sie bitte die E-Mail Addresse des Betreuers an."
        admin_mail = raw_input("Eingabe: ")
        impressum_string = ( \
            "<p><h4>Betreiber</p></h4> \n" \
            + org_name + "</br> \n" + org_part + "</br> \n" \
            + org_street + "</br> \n" + org_city + "</br> \n" \
            + "Tel.: " + org_tel + "</br> \n" + "Fax: " + org_fax + \
            "</br> </p> \n \n"  + "<p><h4>Zuständiger Bearbeiter</h4> \n" \
            + admin_name + "</br> \n" + admin_tel + "</br> \n" + admin_mail \
            + "</p>")
        self.write_impressum(impressum_string)

        
    def write_impressum(self, text):
        impressum_file = open("./template/impressum_personal.html","w")
        impressum_file.write(text)
        impressum_file.close()