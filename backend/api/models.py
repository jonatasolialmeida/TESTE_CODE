from django.db import models
from django.contrib.auth.models import User


class SocialPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="social_posts")
    title = models.CharField(max_length=255, default="Default Title")
    content = models.TextField()
    created_in = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Post by {self.author.username} - {self.title}"


class Comment(models.Model):
    social_post = models.ForeignKey(SocialPost, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_in = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.author.username} in the post {self.social_post.id}"

    class Meta:
        verbose_name_plural = "Comments"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("NEW_COMMENT", "New Comment"),
        ("POST_REMOVED", "Post Removed"),
        ("MENTIONED", "Mentioned User"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    social_post = models.ForeignKey(
        SocialPost,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    content = models.TextField()
    created_in = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification to {self.user.username} - {self.notification_type}"

    class Meta:
        ordering = ["-created_in"]
        verbose_name_plural = "Notifications"
