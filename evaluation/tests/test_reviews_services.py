from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from evaluation.models import Review
from evaluation.serializers import ReviewSerializer


class ReviewsServicesTestCase(TestCase):
    def setUp(self):
        # Creates two different users
        self.first_user = User.objects.create_user(
            username='first_user', password='Amvnfr213!'
        )
        self.second_user = User.objects.create_user(
            username='second_user', password='Amvnfr213!'
        )
        self.third_user = User.objects.create_user(
            username='third_user', password='Amvnfr213!'
        )

        # Assign Reviews to users
        Review.objects.create(
            user=self.first_user,
            rating=4,
            title='Test Review 01',
            summary='Test Review 01 Summary',
            company='Company 01',
            ip_address='127.0.0.1'
        )
        Review.objects.create(
            user=self.second_user,
            rating=2,
            title='Test Review 02',
            summary='Test Review 02 Summary',
            company='Company 02',
            ip_address='127.0.0.1'
        )

        # Retrieves access tokens
        self.client = APIClient()

    def test_list_unauthenticated_reviews(self):
        expected_response = {
            "detail": "Authentication credentials were not provided."
        }
        response = self.client.get(reverse('evaluation:reviews-list'))

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(response.data, expected_response)

    def test_list_wrong_credentials(self):
        expected_response = {
            "detail": 'Given token not valid for any token type',
            "code": "token_not_valid",
            "messages": [
                {
                    "token_class": "AccessToken",
                    "token_type": "access",
                    "message": "Token is invalid or expired"
                }
            ]
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer wrong_token')

        response = self.client.get(
            reverse('evaluation:reviews-list'),
            headers={
                'Authorization': 'Bearer ajksndjkqwnekjnkqj'
            }
        )

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(response.data, expected_response)

    def test_list_first_user_reviews(self):
        # Arrange
        self.client.force_authenticate(self.first_user)
        expected_reviews = Review.objects.filter(
            user=self.first_user
        )
        serializer = ReviewSerializer(expected_reviews, many=True)

        # Act
        response = self.client.get(reverse('evaluation:reviews-list'))

        # Assert
        self.assertEquals(response.data, serializer.data)

    def test_list_second_user_reviews(self):
        # Arrange
        self.client.force_authenticate(self.second_user)
        expected_reviews = Review.objects.filter(
            user=self.second_user
        )
        serializer = ReviewSerializer(expected_reviews, many=True)

        # Act
        response = self.client.get(reverse('evaluation:reviews-list'))

        # Assert
        self.assertEquals(response.data, serializer.data)

    def test_list_third_user_reviews(self):
        # Arrange
        self.client.force_authenticate(self.third_user)
        expected_response = []

        # Act
        response = self.client.get(reverse('evaluation:reviews-list'))

        # Assert
        self.assertEquals(response.data, expected_response)
