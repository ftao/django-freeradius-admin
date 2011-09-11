from django.test import TestCase
from django.test import Client
from django.utils import simplejson as json

class RadGroupTest(TestCase):
    fixtures = ['radcheck-test.json', 'radusergroup-test.json', 'radgroupcheck-test.json']

    def setUp(self):
        self.client = Client()

    def test_getlist(self):
        resp = self.client.get('/api/0/radgroups/')
        expected = ['default', 'trial', 'default-123']
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), expected)


    def test_get(self):
        resp = self.client.get('/api/0/radgroups/trial/')
        expected = {
            "groupname": "trial", 
            "user_count": 2, 
            "attrs": [
                {
                    "attribute": "Simultaneous-Use", 
                    "value": "1", 
                    "op": ":="
                }
            ]
        }
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), expected)
    
