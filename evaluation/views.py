from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from evaluation.serializers import ReviewSerializer, ReviewWriteSerializer


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return self.request.user.reviews.all()

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        request.data['ip_address'] = self.get_client_ip(request)

        serializer = ReviewWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        read_serializer = ReviewSerializer(serializer.instance)
        headers = self.get_success_headers(read_serializer.data)

        return Response(
            ReviewSerializer(serializer.instance).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
