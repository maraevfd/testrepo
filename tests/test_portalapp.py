from django.test import TestCase, Client
from portalapp import models
from django.contrib.auth.models import User
import ddt
import mock


@ddt.ddt
class ExpenseTestClass(TestCase):

    def setUp(self):
        super(ExpenseTestClass, self).__init__()
        self.client = Client()
        self.user = User(first_name="yourone1")
        self.user.save()

    def test_expense_added(self):
        """Test record creation returns 200"""
        response = self.client.post('/add_expense/',
                                    {'category': 'Products',
                                     'title': 'New purchase',
                                     'expense': 20.5})
        self.assertEqual(response.status_code, 200)

    @ddt.data("slug1", "slug2", "slug3")
    def test_slug_created(self, name):
        """Test slug={} created correctyly"""
        response = self.client.post('/add_category/',
                                    {'name': name})
        self.assertEqual(models.Category.objects.get().slug,
                         name)

    @ddt.data(
        ("slu g1", "slug1"),
        ("s lu g 2", "slug2"),
        ("sl ug3", "slug3"),
    )
    @ddt.unpack
    def test_slug_created_correctly(self, name, expected_slug):
        response = self.client.post('/add_category/',
                                    {'name': name})
        self.assertEqual(models.Category.objects.get().slug,
                         expected_slug)

    @staticmethod
    def _create_category():
        category = models.Category(slug='slug',
                                   name='Some name')
        category.save()
        return category

    def test_send_email(self):
        category = self._create_category()

        with mock.patch('portalapp.views.send_mail') as mail_mock:
            response = self.client.post('/' + str(category.id) + '/send/',
                                        {"address": "addr@dd.dd",
                                         "comment": "adsfadsf"})
        mail_mock.assert_called_once()

    @mock.patch('portalapp.views.send_mail')
    def test_send_email_decorated(self, mail_mock):
        category = self._create_category()
        response = self.client.post('/' + str(category.id) + '/send/',
                                    {"address": "addr@dd.dd",
                                     "comment": "adsfadsf"})
        mail_mock.assert_called_once()
