from django.test import TestCase
from djra.freeradius.models import RadUser

class RadUserTest(TestCase):
    multi_db = True
    fixtures = ['radcheck-test.json', 'radusergroup-test.json', 'radacct-test.json']

    def test_properties(self):
        ru = RadUser.objects.get(username='demo')
        self.assertEqual(ru.password, '31415926')
        self.assertEqual(ru.is_active, True)
        #Note: just write ru.groups will not work
        self.assertEqual(list(ru.groups), [u'default'])

    def test_operations(self):
        ru = RadUser.objects.get(username='demo')

        ru.set_password('123')
        ru = RadUser.objects.get(username='demo')
        self.assertEqual(ru.password, '123')

        ru.set_is_active(False)
        ru = RadUser.objects.get(username='demo')
        self.assertEqual(ru.is_active, False)

        ru.set_groups(['abc','other'])
        ru = RadUser.objects.get(username='demo')
        self.assertEqual(list(ru.groups), [u'abc', u'other'])

        ru.update(password='234', is_active=True, groups=['d','e'])
        ru = RadUser.objects.get(username='demo')
        self.assertEqual(ru.password, '234')
        self.assertEqual(ru.is_active, True)
        self.assertEqual(list(ru.groups), [u'd', u'e'])

        ru.update(password='345')
        ru = RadUser.objects.get(username='demo')
        self.assertEqual(ru.is_active, True)
        self.assertEqual(list(ru.groups), [u'd', u'e'])

        ru.update(is_active=False)
        ru = RadUser.objects.get(username='demo')
        self.assertEqual(ru.password, '345')
        self.assertEqual(list(ru.groups), [u'd', u'e'])

        ru.update(groups=['c','d'])
        ru = RadUser.objects.get(username='demo')
        self.assertEqual(ru.password, '345')
        self.assertEqual(ru.is_active, False)


    def test_query(self):
        au = RadUser.objects.all().filter_is_active(1)
        self.assertEqual(len(au), 3)
        su = RadUser.objects.all().filter_is_active(0)
        self.assertEqual(len(su), 1)

        onu = RadUser.objects.all().filter_is_online(1)
        self.assertEqual(len(onu), 1)
        ofu = RadUser.objects.all().filter_is_online(0)
        self.assertEqual(len(ofu), 3)

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

