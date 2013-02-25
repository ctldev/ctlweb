#vim: set fileencoding=utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from frontend.app import ctlweb
from django.test import TestCase
from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf import settings
from django.contrib.auth.models import User

class StatusTest(TestCase):
    urls = 'ctlweb.urls'
    
    def load_url_pattern_names(self, patterns):
        """Retrieve a list of urlpattern names"""
        URL_NAMES = []
        for pat in patterns:
            if pat.__class__.__name__ == 'RegexURLResolver':
                # load patterns from this RegexURLResolver
                self.load_url_pattern_names(pat.url_patterns)
            elif pat.__class__.__name__ ==  'RegexURLPattern':
                # load name from this RegexURLPattern
                if pat.name is not None and pat.name not in URL_NAMES:
                    URL_NAMES.append(pat.name)
        return URL_NAMES

    def test_sites(self):
        admin = User()
        admin.username = "admin"
        admin.email = "test@test.de"
        admin.set_password("test")
        admin.save()
        login = self.client.login(username="admin", password="test")
        self.failUnlessEqual(login, True)
        url_root = __import__(settings.ROOT_URLCONF)
        urls = self.load_url_pattern_names(url_root.urls.urlpatterns)
        for url in urls:
            failed_urls = []
            try:
                reverse_url = reverse(url)
                response = self.client.get(reverse_url)
            except NoReverseMatch, e:
                failed_urls.append(url)
                if url == "auth_login":
                    reverse_url = reverse(url, 
                            kwargs={'username':'admin', 'password': "test"})
                    response = self.client.get(reverse_url)
                    self.failUnlessEqual(response.status_code, 200)
                elif url == "component":
                    reverse_url = reverse(url, args=[1])
                    response = self.client.get(reverse_url)
                    self.failUnlessEqual(response.status_code, 404)
                elif url == "component_receive":
                    token = "abcdefghijklmnopqrstuvwxyz"
                    token += "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890ab"
                    reverse_url = reverse(url, args=[token])
                    response = self.client.get(reverse_url)
                    self.failUnlessEqual(response.status_code, 404)
                else:
                    print url, ":", e
                continue
            self.failUnlessEqual(response.status_code, 200)

    def special_sites(self):
        reversed_urls = dict()
        reversed_urls["c_detail"] = reverse("component_detail",
                kwargs={'comp_id': 1})
        reversed_urls["c_receive"] = reverse("receive_modules", 
                kwargs={'token' : 'asdfe'})
        response = self.client.get(reversed_urls["c_detail"])
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get(reversed_urls["c_receive"])
        self.failUnlessEqual(response.status_code, 404)
