from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from pursuer.models import Man
from pursuer.forms import ManForm
from pursuer.admin import ManAdmin

class MockRequest(object):
    pass


class MockSuperUser(object):
    def has_perm(self, perm):
        return True

request = MockRequest()
request.user = MockSuperUser()


class ManFormTest(TestCase):

    def setUp(self):
        self.man1 = Man.objects.create(
            name='man1',
            follow_ids='2'
        )
        self.man2 = Man.objects.create(
            name='man2',
            follow_ids='3'
        )
        self.man3 = Man.objects.create(
            name='man3',
            follow_ids=''
        )


    def test_valid_data(self):
        form = ManForm({
            'persecuted': [1, 2],
            'pursued': [3],
            'name': 'Man1'
        },
        instance = self.man1
        )
        self.assertTrue(form.is_valid())
        man = form.save()
        self.assertEqual(man.name, "Man1")
        self.assertEqual(man.follow_ids, "1 2")
        self.man3.refresh_from_db()
        self.assertEqual(self.man3.follow_ids, '1')

    def test_blank_data(self):
        form = ManForm({}, instance = self.man1)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['This field is required.'],
            'persecuted': ['This field is required.'],
            'pursued': ['This field is required.'],
        })


class ManAdminTests(TestCase):

    def setUp(self):
        self.man1 = Man.objects.create(
            name='man1',
            follow_ids='2'
        )
        self.man2 = Man.objects.create(
            name='man2',
            follow_ids='3'
        )
        self.man3 = Man.objects.create(
            name='man3',
            follow_ids=''
        )

        self.site = AdminSite()

    # form/fields/fieldsets interaction ##############################

    def test_default_fields(self):
        ma = ManAdmin(Man, self.site)

        self.assertEqual(ma.persecuted_count(self.man1), 1)
        self.assertEqual(ma.persecuted_count(self.man2), 1)
        self.assertEqual(ma.persecuted_count(self.man3), 0)

        self.assertEqual(ma.pursued_count(self.man1), 0)
        self.assertEqual(ma.pursued_count(self.man2), 1)
        self.assertEqual(ma.pursued_count(self.man3), 1)