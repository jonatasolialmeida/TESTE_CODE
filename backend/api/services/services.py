from django.contrib.auth.models import User
from api.models import SocialPost, Comment, Notification


class SocialPostService:
    @staticmethod
    def create_post(author, title, content):
        return SocialPost.objects.create(
            author=author,
            title=title,
            content=content
        )

    @staticmethod
    def update_post(social_post, title, new_content):
        social_post.title = title
        social_post.content = new_content
        social_post.save()
        return social_post

    @staticmethod
    def delete_social_post(social_post):
        social_post.is_active = False
        social_post.save()
        NotificationService.notify_social_post_removed(social_post)


class CommentService:
    @staticmethod
    def create_comment(social_post, author, content):
        comment = Comment.objects.create(
            social_post=social_post,
            author=author,
            content=content
        )
        NotificationService.create_comment_notifications(comment)
        return comment


class NotificationService:
    @staticmethod
    def create_comment_notifications(comment):
        # Notify the social_post's author
        if comment.author != comment.social_post.author:
            Notification.objects.create(
                user=comment.social_post.author,
                social_post=comment.social_post,
                comment=comment,
                notification_type='NEW_COMMENT',
                content=f"{comment.author.username} commented on your post"
            )

        # Notify other commenters
        commenters = Comment.objects.filter(
            social_post=comment.social_post
        ).exclude(
            author__in=[comment.author, comment.social_post.author]
        ).values_list('author', flat=True).distinct()

        for user_id in commenters:
            user = User.objects.get(id=user_id)
            Notification.objects.create(
                user=user,
                social_post=comment.social_post,
                comment=comment,
                notification_type='NEW_COMMENT',
                content=f"{comment.author.username} commented on the post you also commented on"
            )

    @staticmethod
    def notify_social_post_removed(social_post):
        notifications = Notification.objects.filter(
            social_post=social_post,
            read=False
        )

        for notification in notifications:
            notification.notification_type = 'POST_REMOVED'
            notification.content = 'The post was removed by the author'
            notification.save()
