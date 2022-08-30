from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.


User = get_user_model()

class UserTestCast(TestCase):

    def setUp(self):
        user_a = User(username='john', email='john@example.com')
        user_a_pw = '123abc'
        self.user_a_pw = user_a_pw
        user_a.is_staff = True
        user_a.is_superuser = True
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1) 
        self.assertNotEqual(user_count, 0)

    def test_user_password(self):
        user_a = User.objects.get(username="john")
        self.assertTrue(
            user_a.check_password(self.user_a_pw)
        )

    def test_login_url(self):
        login_url = settings.LOGIN_URL
        data = {'username': 'john', 'password': '123abc'}
        response = self.client.post(login_url, data, follow=True)
        status_code = response.status_code
        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, settings.LOGIN_REDIRECT_URL)
        self.assertEqual(status_code, 200)