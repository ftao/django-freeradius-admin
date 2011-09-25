from django.test import TestCase
from django.test import Client
from django.utils import simplejson as json

class DashboardTest(TestCase):
    fixtures = ['radcheck-test.json', 'radusergroup-test.json', 'auth-test.json']

    def setUp(self):
        self.client = Client()

    def test_notlogin(self):
        resp = self.client.get('/radmin/')
        self.assertEqual(resp.status_code, 302)
        
    def test_dashboard(self):
        self.client.login(username='ftao', password='123456')
        resp = self.client.get('/radmin/')
        self.assertEqual(resp.status_code, 200)

