from django.contrib.auth.models import User
from rest_framework.test import APITestCase
import pyotp

class AuthenticationAPITests(APITestCase):
    def setUp(self):
        self.register_url = "/api/auth/register/"
        self.login_url = "/api/auth/login/"
        self.twofa_login_url = "/api/auth/login/2fa/"
        self.enable_2fa_url = "/api/auth/2fa/enable/"
        self.confirm_2fa_url = "/api/auth/2fa/confirm/"

    def test_register_creates_user_and_profile(self):
        response = self.client.post(
            self.register_url,
            {"username": "alice", "email": "alice@example.com", "password": "pass123"},
        )
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username="alice")
        self.assertTrue(hasattr(user, "profile"))

    def test_login_without_2fa_returns_tokens(self):
        User.objects.create_user(username="bob", password="pass123")
        response = self.client.post(
            self.login_url,
            {"username": "bob", "password": "pass123"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_enable_and_confirm_2fa(self):
        user = User.objects.create_user(username="carol", password="pass123")
        self.client.force_authenticate(user=user)
        resp = self.client.post(self.enable_2fa_url)
        self.assertEqual(resp.status_code, 200)
        secret = resp.data["secret"]
        token = pyotp.TOTP(secret).now()
        resp = self.client.post(self.confirm_2fa_url, {"token": token})
        self.assertEqual(resp.status_code, 200)
        user.refresh_from_db()
        self.assertTrue(user.profile.two_factor_enabled)

    def test_login_with_2fa_flow(self):
        user = User.objects.create_user(username="dave", password="pass123")
        self.client.force_authenticate(user=user)
        secret = self.client.post(self.enable_2fa_url).data["secret"]
        token = pyotp.TOTP(secret).now()
        self.client.post(self.confirm_2fa_url, {"token": token})
        self.client.logout()
        resp = self.client.post(self.login_url, {"username": "dave", "password": "pass123"})
        self.assertEqual(resp.status_code, 202)
        token = pyotp.TOTP(secret).now()
        resp = self.client.post(self.twofa_login_url, {"token": token})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("access", resp.data)

    def test_twofa_login_with_invalid_token(self):
        user = User.objects.create_user(username="erin", password="pass123")
        self.client.force_authenticate(user=user)
        secret = self.client.post(self.enable_2fa_url).data["secret"]
        token = pyotp.TOTP(secret).now()
        self.client.post(self.confirm_2fa_url, {"token": token})
        self.client.logout()
        self.client.post(self.login_url, {"username": "erin", "password": "pass123"})
        resp = self.client.post(self.twofa_login_url, {"token": "123456"})
        self.assertEqual(resp.status_code, 400)
