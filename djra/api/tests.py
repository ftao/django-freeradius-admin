"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test import Client
from django.utils import simplejson as json

class RadUserTest(TestCase):
    fixtures = ['radcheck-test.json', 'radusergroup-test.json']

    def setUp(self):
        self.client = Client()

    def test_get(self):
        resp = self.client.get('/api/radusers/demo/')
        expected = {
            "username": "demo", 
            "password": "31415926", 
            "is_valid": True, 
            "groups": [
                "default"
            ]
        }
        self.assertEqual(json.loads(resp.content), expected)

    def test_create_duplicate(self):
        data = {
            "username": "demo", 
            "password": "314159267", 
        }
        resp = self.client.post('/api/radusers/', data=data)
        self.assertEqual(resp.status_code, 409)

    def test_create_empty_pass(self):
        data = {
            "username": "demo2", 
        }
        resp = self.client.post('/api/radusers/', data=data)
        self.assertEqual(resp.status_code, 200)
        ret= json.loads(resp.content)
        self.assertEqual(ret['username'], 'demo2')
        self.assertTrue('password' in ret and len(ret['password']) > 0)
        self.assertTrue(ret['is_valid'])
        self.assertTrue('default' in ret['groups'])

    def test_create_spectific_groups(self):
        data = {
            "username": "demo2", 
            "password" : "1234",
            "groups" : "trial,other,,,,,",
        }
        resp = self.client.post('/api/radusers/', data=data)
        self.assertEqual(resp.status_code, 200)
        ret= json.loads(resp.content)
        self.assertEqual(ret['username'], 'demo2')
        self.assertEqual(ret['password'], '1234')
        self.assertTrue(ret['is_valid'])
        self.assertEqual(ret['groups'], ['trial', 'other'])

    def test_create_default_invalid(self):
        data = {
            "username": "demo2", 
            "is_valid" : "0"
        }
        resp = self.client.post('/api/radusers/', data=data)
        self.assertEqual(resp.status_code, 200)
        ret= json.loads(resp.content)
        self.assertEqual(ret['username'], 'demo2')
        self.assertTrue(not ret['is_valid'])


    def test_update_404(self):
        data = {
            "username": "demo2", 
            "is_valid" : "0"
        }
        resp = self.client.put('/api/radusers/', data=data)
        self.assertEqual(resp.status_code, 404)


    def test_update_nothing(self):

        resp = self.client.get('/api/radusers/demo/')
        old_ret = json.loads(resp.content)

        resp = self.client.put('/api/radusers/demo/', data={})
        ret= json.loads(resp.content)

        self.assertEqual(old_ret, ret)


    def test_update_pass_username_as_url(self):
        data = {
            "is_valid" : "0"
        }
        resp = self.client.put('/api/radusers/demo/', data=data)
        self.assertEqual(resp.status_code, 200)
        ret= json.loads(resp.content)
        self.assertEqual(ret['username'], 'demo')
        self.assertTrue(not ret['is_valid'])

        resp = self.client.put('/api/radusers/demo/', data={'is_valid' : '1'})
        ret= json.loads(resp.content)
        self.assertEqual(ret['username'], 'demo')
        self.assertTrue(ret['is_valid'])

    def test_update_password(self):
        data = {
            "username" : "demo",
            "password" : "123456",
        }
        resp = self.client.put('/api/radusers/', data=data)
        self.assertEqual(resp.status_code, 200)
        ret= json.loads(resp.content)
        self.assertEqual(ret['username'], 'demo')
        self.assertTrue(ret['is_valid'])
        self.assertEqual(ret['password'], "123456")

    
    def test_update_groups(self):
        data = {
            "username" : "demo",
            "groups" : "trial,other",
        }
        resp = self.client.put('/api/radusers/', data=data)
        self.assertEqual(resp.status_code, 200)
        ret= json.loads(resp.content)
        self.assertEqual(ret['username'], 'demo')
        self.assertEqual(ret['groups'], ["trial", "other"])


    def test_update(self):
        data = {
            "username" : "demo",
            "is_valid" : "0",
            "password" : "123456",
            "groups" : "trial,other",
        }
        resp = self.client.put('/api/radusers/', data=data)
        self.assertEqual(resp.status_code, 200)
        ret= json.loads(resp.content)
        self.assertEqual(ret['username'], 'demo')
        self.assertTrue(not ret['is_valid'])
        self.assertEqual(ret['password'], "123456")
        self.assertEqual(ret['groups'], ["trial", "other"])

