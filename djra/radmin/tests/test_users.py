from django.test import TestCase
from django.test import Client
from django.utils import simplejson as json

class UsersTest(TestCase):
    fixtures = ['radcheck-test.json', 'radusergroup-test.json',
                'radgroupcheck-test.json', 'radacct-test.json', 'auth-test.json']

    def setUp(self):
        self.client = Client()

    def test_users_not_login(self):
        resp = self.client.get('/radmin/users/')
        self.assertEqual(resp.status_code, 302)

    def test_users(self):
        self.client.login(username='ftao', password='123456')
        resp = self.client.get('/radmin/users/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.count(u'cell-username'), 4)

    def test_user_detail(self):
        self.client.login(username='ftao', password='123456')
        resp = self.client.post('/radmin/user/demo/',
            {'username' : 'demo', 'password': '1', 'is_suspended' : 'on', 'groups' : 'default,test'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], 'http://testserver/radmin/user/demo/')

        resp = self.client.get('/radmin/user/demo/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form'].data, 
            {u'username': 'demo', u'is_suspended': True, u'groups' : 'default,test', u'password' : '1'})

    def test_user_session(self):
        self.client.login(username='ftao', password='123456')
        resp = self.client.get('/radmin/user/demo/sessions/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.count(u'<tr'), 5)
