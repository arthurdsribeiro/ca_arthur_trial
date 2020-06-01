from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status


class TokenVerificationTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='test_user', password='Amvnfr213!')
        self.client = Client()

    def test_login_no_data(self):
        expected_response = {
            "username": [
                "This field is required."
            ],
            "password": [
                "This field is required."
            ]
        }

        response = self.client.post(reverse('evaluation:token_obtain_pair'))

        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEquals(expected_response, response.data)

    def test_incorrect_password_test_user(self):
        expected_response = {
            "detail": "No active account found with the given credentials"
        }
        request_body = {
            "username": "test_user",
            "password": "123456"
        }

        response = self.client.post(
            reverse('evaluation:token_obtain_pair'),
            request_body
        )

        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEquals(expected_response, response.data)

    def test_correct_password_test_user(self):
        request_body = {
            "username": "test_user",
            "password": "Amvnfr213!"
        }

        response = self.client.post(
            reverse('evaluation:token_obtain_pair'),
            request_body
        )

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token_success(self):
        # Arrange
        login_request_body = {
            "username": "test_user",
            "password": "Amvnfr213!"
        }
        login_response = self.client.post(
            reverse('evaluation:token_obtain_pair'),
            login_request_body
        )
        refresh_token = login_response.json().get('refresh')
        refresh_request_body = {
            'refresh': refresh_token
        }

        # Act
        response = self.client.post(
            reverse('evaluation:token_refresh'),
            refresh_request_body
        )

        # Assert
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertIn('access', response.data)

    def test_refresh_token_error(self):
        # Arrange
        login_request_body = {
            "username": "test_user",
            "password": "Amvnfr213!"
        }
        response = self.client.post(
            reverse('evaluation:token_obtain_pair'),
            login_request_body
        )
        refresh_token = response.json().get('refresh')
        refresh_request_body = {
            'refresh': refresh_token + "a"
        }
        expected_response = {
            "detail": "Token is invalid or expired",
            "code": "token_not_valid"
        }

        # Act
        response = self.client.post(
            reverse('evaluation:token_refresh'),
            refresh_request_body
        )

        # Assert
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEquals(expected_response, response.data)

    def test_verify_token_success(self):
        # Arrange
        login_request_body = {
            "username": "test_user",
            "password": "Amvnfr213!"
        }
        login_response = self.client.post(
            reverse('evaluation:token_obtain_pair'),
            login_request_body
        )
        access_token = login_response.json().get('access')
        verify_request_body = {
            'token': access_token
        }

        # Act
        response = self.client.post(
            reverse('evaluation:token_verify'),
            verify_request_body
        )

        # Assert
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals({}, response.data)

    def test_verify_token_error(self):
        # Arrange
        login_request_body = {
            "username": "test_user",
            "password": "Amvnfr213!"
        }
        response = self.client.post(
            reverse('evaluation:token_obtain_pair'),
            login_request_body
        )
        access_token = response.json().get('refresh')
        refresh_request_body = {
            'token': access_token + "a"
        }
        expected_response = {
            "detail": "Token is invalid or expired",
            "code": "token_not_valid"
        }

        # Act
        response = self.client.post(
            reverse('evaluation:token_verify'),
            refresh_request_body
        )

        # Assert
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEquals(expected_response, response.data)
