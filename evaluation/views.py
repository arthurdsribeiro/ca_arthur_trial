from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from evaluation.serializers import ReviewSerializer


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return self.request.user.reviews.all()
