from django.test import TestCase
from django.test import Client
from django.utils import simplejson as json

class RadAcctTest(TestCase):
    fixtures = ['radacct-test.json',]

    def setUp(self):
        self.client = Client()

    def test_getlist(self):
        resp = self.client.get('/api/0/radusers/demo/acct/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(json.loads(resp.content)), 4)


    def test_get_connected(self):
        resp = self.client.get('/api/0/radusers/demo/acct/?type=connected')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(json.loads(resp.content)), 2)
