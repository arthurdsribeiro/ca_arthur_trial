from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from evaluation.views import (
    ReviewViewSet,
)
from rest_framework import routers


app_name = 'evaluation'

router = routers.SimpleRouter()
router.register(r'reviews', ReviewViewSet, 'reviews')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-token/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += router.urls
