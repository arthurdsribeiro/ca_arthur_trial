from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from evaluation.models import Review
from evaluation.serializers import ReviewSerializer, ReviewWriteSerializer
from drf_yasg.utils import swagger_auto_schema


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_anonymous:
            return self.request.user.reviews.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewWriteSerializer
        return ReviewSerializer

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def perform_create(self, serializer):
        review = Review(**serializer.data)
        review.user = self.request.user
        review.ip_address = self.get_client_ip(self.request)
        review.save()
        return review

    @swagger_auto_schema(responses={200: ReviewSerializer()})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            ReviewSerializer(review).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
