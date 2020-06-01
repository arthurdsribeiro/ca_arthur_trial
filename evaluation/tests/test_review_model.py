from django.test import TestCase
from evaluation.models import Review, User


class ReviewModelTestCase(TestCase):
    def setUp(self):
        self.first_user = User.objects.create_user(
            username='first_user', password='Amvnfr213!'
        )

        self.review1 = Review.objects.create(
            user=self.first_user,
            rating=4,
            title='Test Review 01',
            summary='Test Review 01 Summary',
            company='Company 01',
            ip_address='127.0.0.1'
        )
        self.review2 = Review.objects.create(
            user=self.first_user,
            rating=2,
            title='Test Review 02',
            summary='Test Review 02 Summary',
            company='Company 02',
            ip_address='127.0.0.1'
        )

    def test_str_equals_title(self):
        self.assertEquals(str(self.review1), 'Test Review 01')
        self.assertEquals(str(self.review2), 'Test Review 02')
