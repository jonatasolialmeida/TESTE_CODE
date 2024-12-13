from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.views import PostViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]
