from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.views import SocialPostViewSet, NotificationViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'social-posts', SocialPostViewSet, basename='socialpost')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('', include(router.urls)),
]
