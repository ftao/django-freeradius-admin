from django.test import TestCase
from django.test import Client
from django.utils import simplejson as json

class GroupsTest(TestCase):
    multi_db = True
    fixtures = ['radcheck-test.json', 'radusergroup-test.json',
                'radgroupcheck-test.json', 'auth-test.json']

    def setUp(self):
        self.client = Client()

    def test_not_login(self):
        resp = self.client.get('/radmin/groups/')
        self.assertEqual(resp.status_code, 302)
        
    def test_groups(self):
        self.client.login(username='ftao', password='123456')
        resp = self.client.get('/radmin/groups/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['groups']), 3)

    def test_group_detail(self):
        self.client.login(username='ftao', password='123456')
        resp = self.client.post('/radmin/group/default/' , {'groupname' : 'default', 'simultaneous_use': u'4'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], 'http://testserver/radmin/group/default/')

        resp = self.client.get('/radmin/group/default/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form'].data, {'groupname': u'default', 'simultaneous_use': u'4'})

