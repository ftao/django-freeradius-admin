from django.test import TestCase
from django.test import Client
from django.utils import simplejson as json
from djra.api.models import RadUser

class RadUserTest(TestCase):
    multi_db = True
    fixtures = ['radcheck-test.json', 'radusergroup-test.json']

    def test_properties(self):
        ru = RadUser.objects.get(username='demo')
        self.assertEqual(ru.password, '31415926')
        self.assertEqual(ru.is_suspended, False)
        #Note: just write ru.groups will not work
        self.assertEqual(list(ru.groups), [u'default'])

    def test_operations(self):
        ru = RadUser.objects.get(username='demo')

        ru.change_password('123')
        ru = RadUser.objects.get(username='demo')
        self.assertEqual(ru.password, '123')

        ru.toggle_suspended(True)
        ru = RadUser.objects.get(username='demo')
        self.assertEqual(ru.is_suspended, True)

        ru.change_groups(['abc','other'])
        ru = RadUser.objects.get(username='demo')
        self.assertEqual(list(ru.groups), [u'abc', u'other'])

        ru.update(password='234', is_suspended=False, groups=['d','e'])
        ru = RadUser.objects.get(username='demo')
        self.assertEqual(ru.password, '234')
        self.assertEqual(ru.is_suspended, False)
        self.assertEqual(list(ru.groups), [u'd', u'e'])

        ru.update(password='345')
        ru = RadUser.objects.get(username='demo')
        self.assertEqual(ru.is_suspended, False)
        self.assertEqual(list(ru.groups), [u'd', u'e'])

        ru.update(is_suspended=True)
        ru = RadUser.objects.get(username='demo')
        self.assertEqual(ru.password, '345')
        self.assertEqual(list(ru.groups), [u'd', u'e'])

        ru.update(groups=['c','d'])
        ru = RadUser.objects.get(username='demo')
        self.assertEqual(ru.password, '345')
        self.assertEqual(ru.is_suspended, True)


    def test_query(self):
        au = RadUser.objects.query_active_user()
        self.assertEqual(len(au), 3)
        su = RadUser.objects.query_suspended_user()
        self.assertEqual(len(su), 1)

        allu = RadUser.objects.all()
        self.assertEqual(len(allu), 4)

    def test_count_info(self):
        self.assertEqual(RadUser.objects.count_info(), {'active': 3, 'total': 4, 'suspended': 1})

    def test_create(self):
        u = RadUser.objects.create(username='d1', password='abc')
        self.assertEqual(u.password, 'abc')
        self.assertEqual(u.username, 'd1')

       
    def test_get_or_create(self):
        u,created = RadUser.objects.get_or_create(username='d1', defaults={'password':'abc'})
        self.assertTrue(created)
        self.assertEqual(u.password, 'abc')
        self.assertEqual(u.username, 'd1')

        u,created = RadUser.objects.get_or_create(username='demo', defaults={'password':'abc'})
        self.assertTrue(not created)
        self.assertNotEqual(u.password, 'abc')
        self.assertEqual(u.username, 'demo')

