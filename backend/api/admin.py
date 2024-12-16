from django.contrib import admin
from .models import SocialPost, Comment, Notification

@admin.register(SocialPost)
class SocialPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'created_in', 'is_active')
    search_fields = ('title', 'content')
    list_filter = ('is_active', 'created_in')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'social_post', 'author', 'created_in')
    search_fields = ('content',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'notification_type', 'created_in', 'read')
    list_filter = ('notification_type', 'read', 'created_in')
