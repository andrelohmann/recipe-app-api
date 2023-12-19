"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from django.core import mail


USERS_URL = reverse('authentication:user-list')
USERS_DETAIL_URL = reverse('authentication:user-detail', args=["pk"])
USERS_ACTIVATION_URL = reverse('authentication:user-activation')
USERS_RESEND_ACTIVATION_URL = reverse('authentication:user-resend-activation')
USERS_SET_USERNAME_URL = reverse('authentication:user-set-username')
USERS_RESET_USERNAME_URL = reverse('authentication:user-reset-username')
USERS_RESET_USERNAME_CONFIRM_URL = reverse('authentication:user-reset-username-confirm')
USERS_SET_PASSWORD_URL = reverse('authentication:user-set-password')
USERS_RESET_PASSWORD_URL = reverse('authentication:user-reset-password')
USERS_RESET_PASSWORD_CONFIRM_URL = reverse('authentication:user-reset-password-confirm')
USERS_ME_URL = reverse('authentication:user-me')
JWT_CREATE_URL = reverse('authentication:jwt-create')
JWT_REFRESH_URL = reverse('authentication:jwt-refresh')
JWT_VERIFY_URL = reverse('authentication:jwt-verify')
JWT_LOGOUT_URL = reverse('authentication:logout')

TEST_USER = payload = {
    'email': 'test@example.com',
    'password': 'Test.P@ss.123!',
    'first_name': 'Test',
    'last_name': 'User',
}
SIMPLE_PASSWORD_USER = payload = {
    'email': 'test@example.com',
    'password': 'Test123',
    'first_name': 'Test',
    'last_name': 'User',
}
SUPER_USER = payload = {
    'email': 'super@example.com',
    'password': 'Test.P@ss.123!',
    'first_name': 'Super',
    'last_name': 'User',
}

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

class RoutesTest(TestCase):
    """Test the URL shortcuts."""

    def test_jwt_routes(self):
        """Test the jwt shortcuts."""
        self.assertEqual(JWT_CREATE_URL, '/api/v0/auth/jwt/create/')
        self.assertEqual(JWT_REFRESH_URL, '/api/v0/auth/jwt/refresh/')
        self.assertEqual(JWT_VERIFY_URL, '/api/v0/auth/jwt/verify/')
        self.assertEqual(JWT_LOGOUT_URL, '/api/v0/auth/logout/')

    def test_users_routes(self):
        """Test the users shortcuts."""
        self.assertEqual(USERS_URL, '/api/v0/auth/users/')
        self.assertEqual(USERS_DETAIL_URL, '/api/v0/auth/users/pk/')
        self.assertEqual(USERS_ACTIVATION_URL, '/api/v0/auth/users/activation/')
        self.assertEqual(USERS_RESEND_ACTIVATION_URL, '/api/v0/auth/users/resend_activation/')
        self.assertEqual(USERS_SET_USERNAME_URL, '/api/v0/auth/users/set_email/')
        self.assertEqual(USERS_RESET_USERNAME_URL, '/api/v0/auth/users/reset_email/')
        self.assertEqual(USERS_RESET_USERNAME_CONFIRM_URL, '/api/v0/auth/users/reset_email_confirm/')
        self.assertEqual(USERS_SET_PASSWORD_URL, '/api/v0/auth/users/set_password/')
        self.assertEqual(USERS_RESET_PASSWORD_URL, '/api/v0/auth/users/reset_password/')
        self.assertEqual(USERS_RESET_PASSWORD_CONFIRM_URL, '/api/v0/auth/users/reset_password_confirm/')
        self.assertEqual(USERS_ME_URL, '/api/v0/auth/users/me/')


class PublicUserApiTests(APITestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = dict(TEST_USER, re_password=TEST_USER['password'])
        res = self.client.post(USERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=TEST_USER['email'])
        self.assertTrue(user.check_password(TEST_USER['password']))
        self.assertEqual(user.first_name, TEST_USER['first_name'])
        self.assertEqual(user.last_name, TEST_USER['last_name'])
        self.assertNotIn('password', res.data)

    def test_user_email_exists_error(self):
        """Test error returned if user with email exists."""
        create_user(**TEST_USER)
        payload = dict(TEST_USER, re_password=TEST_USER['password'])
        res = self.client.post(USERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_simple(self):
        """Test an error is returned if password is too simple."""
        payload = dict(SIMPLE_PASSWORD_USER, re_password=SIMPLE_PASSWORD_USER['password'])

        res = self.client.post(USERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_inactive_user_error(self):
        """Test fail generate token for inactive credentials."""
        payload = dict(TEST_USER, re_password=TEST_USER['password'])

        res = self.client.post(USERS_URL, payload)

        payload = {
            'email': TEST_USER['email'],
            'password': TEST_USER['password'],
        }
        res = self.client.post(JWT_CREATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('refresh', res.data)
        self.assertNotIn('access', res.data)

    def test_create_token_for_active_user(self):
        """Test generate token for active credentials."""
        payload = dict(TEST_USER, re_password=TEST_USER['password'])

        res = self.client.post(USERS_URL, payload)

        payload = {
            'email': TEST_USER['email'],
            'password': TEST_USER['password'],
        }
        res = self.client.post(JWT_CREATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('refresh', res.data)
        self.assertNotIn('access', res.data)

        self.assertEqual(len(mail.outbox), 1)
        # print(mail.outbox[0].body)
        email_lines = mail.outbox[0].body.splitlines()
        activation_line = [l for l in email_lines if "http://testserver/activation/" in l][0]
        activation_link = activation_line.split("/activation/")[1]
        activation_uid = activation_link.split("/")[0]
        activation_token = activation_link.split("/")[1]
        # print(activation_token)

        res = self.client.post(USERS_ACTIVATION_URL, {"uid": activation_uid, "token": activation_token})

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        res = self.client.post(JWT_CREATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', res.data)
        self.assertIn('access', res.data)



#     def test_create_token_bad_creadentials(self):
#         """Test returns error if credentials invalid."""
#         user_details = {
#             'email': 'test@example.com',
#             'password': 'Test.P@ss.123!',
#             'name': 'Test name',
#         }
#         create_user(**user_details)

#         payload = {
#             'email': user_details['email'],
#             'password': 'badpassword',
#         }
#         res = self.client.post(TOKEN_URL, payload)

#         self.assertNotIn('token', res.data)
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_create_token_blank_password(self):
#         """Test posting a blank password returns an errror."""
#         user_details = {
#             'email': 'test@example.com',
#             'password': 'Test.P@ss.123!',
#             'name': 'Test name',
#         }
#         # create_user(**user_details)
#         payload = {
#             'email': user_details['email'],
#             'password': '',
#         }
#         res = self.client.post(TOKEN_URL, payload)

#         self.assertNotIn('token', res.data)
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_retrieve_user_unauthorized(self):
#         """Test authentication is required for users."""
#         res = self.client.get(ME_URL)

#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# class PrivateUserApiTests(TestCase):
#     """Test API requests, that requite authentication."""

#     def setUp(self):
#         self.user = create_user(
#             email='test@example.com',
#             password='Test.P@ssw0rd.247!',
#             name='test Name',
#         )
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)

#     def test_retrieve_profile_success(self):
#         """Test retrieving profile for logged in user."""
#         res = self.client.get(ME_URL)

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, {
#             'name': self.user.name,
#             'email': self.user.email,
#         })

#     def test_post_me_not_allowed(self):
#         """Test POST is not allowed for the me endpoint."""
#         res = self.client.post(ME_URL, {})

#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

#     def test_update_user_profile(self):
#         """Test updating the user profile for the authenticated user."""
#         payload = {
#             'name': 'Updated Name',
#             'password': 'New.P@ssword.123?',
#         }
#         res = self.client.patch(ME_URL, payload)

#         self.user.refresh_from_db()

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(self.user.name, payload['name'])
#         self.assertTrue(self.user.check_password(payload['password']))


# # https://saasitive.com/tutorial/django-rest-framework-register-user-email-verification/
# from django.core import mail
# from rest_framework import status
# from rest_framework.test import APITestCase

# class AccountsTestCase(APITestCase):

#     register_url = "/api/auth/register/"
#     verify_email_url = "/api/auth/register/verify-email/"
#     login_url = "/api/auth/login/"

#     def test_register(self):

#         # register data
#         data = {
#             "email": "user2@example-email.com",
#             "password1": "verysecret",
#             "password2": "verysecret",
#         }
#         # send POST request to "/api/auth/register/"
#         response = self.client.post(self.register_url, data)
#         # check the response status and data
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.json()["detail"], "Verification e-mail sent.")

#         # try to login - should fail, because email is not verified
#         login_data = {
#             "email": data["email"],
#             "password": data["password1"],
#         }
#         response = self.client.post(self.login_url, login_data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertTrue(
#             "E-mail is not verified." in response.json()["non_field_errors"]
#         )

#         # expected one email to be send
#         # parse email to get token
#         self.assertEqual(len(mail.outbox), 1)
#         email_lines = mail.outbox[0].body.splitlines()
#         activation_line = [l for l in email_lines if "verify-email" in l][0]
#         activation_link = activation_line.split("go to ")[1]
#         activation_key = activation_link.split("/")[4]

#         response = self.client.post(self.verify_email_url, {"key": activation_key})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.json()["detail"], "ok")

#         # lets login after verification to get token key
#         response = self.client.post(self.login_url, login_data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue("key" in response.json())