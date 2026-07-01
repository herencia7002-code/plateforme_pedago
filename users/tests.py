from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# create your tests here.

class InscriptionViewTest(TestCase):
    def test_can_create_account(self):
        response = self.client.post(
            reverse('inscription'),
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'password1': 'StrongPass123',
                'password2': 'StrongPass123',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username='alice').exists())


class ConnexionViewTest(TestCase):
    def test_can_login_with_created_account(self):
        user = get_user_model().objects.create_user(
            username='bob',
            email='bob@example.com',
            password='StrongPass123',
        )

        response = self.client.post(
            reverse('connexion'),
            {
                'username': 'bob',
                'password': 'StrongPass123',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user, user)
