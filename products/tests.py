from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Mugs

# Create your tests here.


User = get_user_model()


class ProductTestCase(TestCase):

    def setUp(self):
        user_a = User(username='john', email='john@balance.com')
        user_a_pw = 'abc123'
        self.user_a_pw = user_a_pw
        user_a.is_staff = True
        user_a.is_superuser = False

        user_a.save()
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a
        user_b = User.objects.create_user('user_2', 'john2@balance.com', '123abc')
        self.user_b = user_b

    def test_user_count(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 2)

    def test_invalid_request(self):
        self.client.login(username=self.user_b.username, password='123abc')
        response = self.client.post('mugs/create', {'title': 'valid test'})
        self.assertNotEqual(response.status_code, 200)

    def test_invalid_request(self):
        self.client.login(username=self.user_a.username, password='abc123')
        response = self.client.post('mugs/create', {'title': 'valid test'})
        self.assertNotEqual(response.status_code, 200)
