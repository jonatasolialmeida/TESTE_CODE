from django.contrib.auth.models import User
from api.models import Post, Comment, Notification

class PostService:
    @staticmethod
    def create_post(author, title, content):
        return Post.objects.create(
            author=author,
            title=title,
            content=content
        )

    @staticmethod
    def update_post(post, title, new_content):
        post.title = title
        post.content = new_content
        post.save()
        return post

    @staticmethod
    def delete_post(post):
        post.is_active = False
        post.save()
        NotificationService.notify_post_removed(post)

class CommentService:
    @staticmethod
    def create_comment(post, author, content):
        comment = Comment.objects.create(
            post=post,
            author=author,
            content=content
        )
        NotificationService.create_comment_notifications(comment)
        return comment

class NotificationService:
    @staticmethod
    def create_comment_notifications(comment):
        # Notify the post's author
        if comment.author != comment.post.author:
            Notification.objects.create(
                user=comment.post.author,
                post=comment.post,
                comment=comment,
                notification_type='NEW_COMMENT',
                content=f"{comment.author.username} commented on your post"
            )

        # Notify other commenters
        commenters = Comment.objects.filter(
            post=comment.post
        ).exclude(
            author__in=[comment.author, comment.post.author]
        ).values_list('author', flat=True).distinct()

        for user_id in commenters:
            user = User.objects.get(id=user_id)
            Notification.objects.create(
                user=user,
                post=comment.post,
                comment=comment,
                notification_type='NEW_COMMENT',
                content=f"{comment.author.username} commented on the post you also commented on"
            )

    @staticmethod
    def notify_post_removed(post):
        notifications = Notification.objects.filter(
            post=post,
            read=False
        )

        for notification in notifications:
            notification.notification_type = 'POST_REMOVED'
            notification.content = 'The post was removed by the author'
            notification.save()
