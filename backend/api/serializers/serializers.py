from rest_framework import serializers
from api.models import Post, Comment, Notification
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_in']
        read_only_fields = ['id', 'created_in']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    total_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 
            'author', 
            'title',
            'content', 
            'created_in', 
            'update_on', 
            'comments',
            'total_comments'
        ]
        read_only_fields = ['id', 'created_in', 'update_on']

    def get_total_comments(self, obj):
        return obj.comments.count()

class NotificationSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 
            'user', 
            'post', 
            'notification_type', 
            'content', 
            'created_in', 
            'read'
        ]
