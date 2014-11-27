from django.test import TestCase
from djra.freeradius.api import RadUserResource,RadGroupResource
from djra.freeradius.models import RadUser
from tastypie.bundle import Bundle
from tastypie.exceptions import NotFound

class RadUserResourceTest(TestCase):
    multi_db = True
    fixtures = ['radcheck-test.json', 'radusergroup-test.json', 'radacct-test.json']

    def test_obj_create(self):
        rr = RadUserResource()
        b = Bundle(data={'username' : 'abc', 'password' : '123445', 'is_active' : True, 'groups' : ['default']})
        ru = rr.obj_create(b)

        self.assertEqual(ru.password, '123445')
        self.assertEqual(ru.is_active, True)
        self.assertEqual(list(ru.groups), ['default'])

    def test_obj_create_gen_password(self):
        rr = RadUserResource()
        b = Bundle(data={'username' : 'abc', 'is_active' : True, 'groups' : ['default']})
        ru = rr.obj_create(b)

        self.assertTrue(ru.password)
 

    def test_obj_update(self):
        ru = RadUser.objects.get(username='demo')
        self.assertEqual(ru.password, '31415926')
        self.assertEqual(ru.is_active, True)
        self.assertEqual(list(ru.groups), [u'default'])

        rr = RadUserResource()
        b = Bundle(data={'password' : 'newpassword', 'is_active' : False, 'groups' : ['default2']})
        ru = rr.obj_update(b, username='demo')

        self.assertEqual(ru.password, 'newpassword')
        self.assertEqual(ru.is_active, False)
        self.assertEqual(list(ru.groups), [u'default2'])



class RadGroupResourceTest(TestCase):
    multi_db = True
    fixtures = ['radcheck-test.json', 'radusergroup-test.json', 'radacct-test.json', 'radgroupcheck-test.json']

    def test_obj_get_list(self):
        rr = RadGroupResource()
        obj_list = rr.obj_get_list()
        self.assertEqual(len(obj_list), 2)
        self.assertEqual(obj_list[0].groupname, 'default')

    def test_obj_get(self):
        rr = RadGroupResource()
        obj = rr.obj_get(None, pk='default')
        self.assertEqual(obj.groupname, 'default')

        self.assertRaises(NotFound, rr.obj_get, None, pk='default2')
