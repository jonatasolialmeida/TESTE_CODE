from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from api.models import SocialPost, Comment, Notification
from api.serializers.serializers import (
    SocialPostSerializer,
    CommentSerializer,
    NotificationSerializer,
)
from api.services.services import (
    SocialPostService,
    CommentService,
    NotificationService,
)


class SocialPostViewSet(viewsets.ModelViewSet):
    queryset = SocialPost.objects.filter(is_active=True)
    serializer_class = SocialPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        social_post = self.get_object()

        if social_post.author != request.user:
            return Response(
                {"error": "You do not have permission to delete this post"},
                status=status.HTTP_403_FORBIDDEN,
            )

        SocialPostService.delete_social_post(social_post)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        social_post = self.get_object()

        if social_post.author != request.user:
            return Response(
                {"error": "You do not have permission to edit this post"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(social_post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["POST"], permission_classes=[permissions.IsAuthenticated])
    def comment(self, request, pk=None):
        social_post = self.get_object()
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            comment = CommentService.create_comment(
                social_post=social_post,
                author=request.user,
                content=serializer.validated_data["content"],
            )
            return Response(
                CommentSerializer(comment).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user,
            read=False,
        )

    @action(detail=True, methods=["PATCH"], permission_classes=[permissions.IsAuthenticated])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()

        if notification.user != request.user:
            return Response(
                {"error": "You do not have permission to mark this notification"},
                status=status.HTTP_403_FORBIDDEN,
            )

        notification.read = True
        notification.save()
        return Response(self.get_serializer(notification).data)
