from django.test import TestCase
from evaluation.serializers import ReviewSerializer
from evaluation.models import Review, User


class ReviewSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            first_name='Test',
            password='123456'
        )
        self.review1 = Review.objects.create(
            user=self.user,
            rating=4,
            title='Test Review 01',
            summary='Test Review 01 Summary',
            company='Company 01',
            ip_address='127.0.0.1'
        )

    def test_review_serializer(self):
        expected_data = {
            'id': self.review1.id,
            'title': 'Test Review 01',
            'summary': 'Test Review 01 Summary',
            'rating': 4,
            'company': 'Company 01',
            'ip_address': '127.0.0.1',
            'date': self.review1.date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name
            }
        }
        serializer = ReviewSerializer(self.review1)

        self.assertEquals(serializer.data, expected_data)
