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
        self.review1 = Review.objects.create(
            user=self.first_user,
            rating=4,
            title='Test Review 01',
            summary='Test Review 01 Summary',
            company='Company 01',
            ip_address='127.0.0.1'
        )
        self.review2 = Review.objects.create(
            user=self.second_user,
            rating=2,
            title='Test Review 02',
            summary='Test Review 02 Summary',
            company='Company 02',
            ip_address='127.0.0.1'
        )

        # Client object to perform requests
        self.client = APIClient()

    def test_list_unauthenticated_reviews(self):
        # Arrange
        expected_response = {
            "detail": "Authentication credentials were not provided."
        }

        # Act
        response = self.client.get(reverse('evaluation:reviews-list'))

        # Assert
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(response.data, expected_response)

    def test_list_wrong_credentials(self):
        # Arrange
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

        # Act
        response = self.client.get(
            reverse('evaluation:reviews-list'),
            headers={
                'Authorization': 'Bearer ajksndjkqwnekjnkqj'
            }
        )

        # Assert
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

    def test_retrive_review_first_user_success(self):
        # Arrange
        serializer = ReviewSerializer(self.review1)
        self.client.force_authenticate(self.first_user)

        # Act
        response = self.client.get(
            reverse('evaluation:reviews-detail', args=[self.review1.id])
        )

        # Assert
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_retrive_review_second_user_success(self):
        # Arrange
        serializer = ReviewSerializer(self.review2)
        self.client.force_authenticate(self.second_user)

        # Act
        response = self.client.get(
            reverse('evaluation:reviews-detail', args=[self.review2.id])
        )

        # Assert
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_retrive_review_unrelated_to_first_user(self):
        # Arrange
        self.client.force_authenticate(self.first_user)

        # Act
        response = self.client.get(
            reverse('evaluation:reviews-detail', args=[self.review2.id])
        )

        # Assert
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_not_available(self):
        # Arrange
        self.client.force_authenticate(self.first_user)

        # Act
        response = self.client.delete(
            reverse('evaluation:reviews-detail', args=[self.review1.id])
        )

        # Assert
        self.assertEquals(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_create_review_success(self):
        # Arrange
        self.client.force_authenticate(self.first_user)
        reviews_before_insert = self.first_user.reviews.count()

        new_review = Review()
        new_review.title = 'Title New'
        new_review.summary = 'Summary New'
        new_review.rating = 5
        new_review.company = 'New Company'

        serializer = ReviewSerializer(new_review)

        # Act
        response = self.client.post(
            reverse('evaluation:reviews-list'),
            serializer.data,
        )

        # Assert
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(1, reviews_before_insert)
        self.assertEquals(
            2, Review.objects.filter(user=self.first_user).count()
        )

    def test_create_review_success_forwarded_ip(self):
        # Arrange
        self.client.force_authenticate(self.first_user)
        reviews_before_insert = self.first_user.reviews.count()

        new_review = Review()
        new_review.title = 'Title New'
        new_review.summary = 'Summary New'
        new_review.rating = 5
        new_review.company = 'New Company'

        serializer = ReviewSerializer(new_review)

        # Act
        response = self.client.post(
            reverse('evaluation:reviews-list'),
            serializer.data,
            HTTP_X_FORWARDED_FOR="8.8.8.8"
        )

        # Assert
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(1, reviews_before_insert)
        self.assertEquals(
            2, Review.objects.filter(user=self.first_user).count()
        )

    def test_create_view_wrong_rating(self):
        # Arrange
        self.client.force_authenticate(self.first_user)
        reviews_before_insert = self.first_user.reviews.count()

        new_review = Review()
        new_review.title = 'Title New'
        new_review.summary = 'Summary New'
        new_review.rating = 10
        new_review.company = 'New Company'

        serializer = ReviewSerializer(new_review)

        # Act
        response = self.client.post(
            reverse('evaluation:reviews-list'),
            serializer.data,
        )

        # Assert
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(1, reviews_before_insert)
        self.assertEquals(
            1, Review.objects.filter(user=self.first_user).count()
        )
