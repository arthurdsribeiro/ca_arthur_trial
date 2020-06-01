from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (
    MinValueValidator, MaxValueValidator
)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    summary = models.TextField(max_length=10000)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    company = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
