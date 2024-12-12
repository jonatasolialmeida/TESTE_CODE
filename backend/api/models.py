import uuid
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )
    content = models.TextField()
    created_in = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Post de {self.author.username} - {self.created_in}"

class Comment(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    content = models.TextField()
    created_in = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Comentário de {self.author.username} no post {self.post.id}"

    class Meta:
        verbose_name_plural = "Comentários"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('NOVO_COMENTARIO', 'Novo Comentário'),
        ('POST_REMOVIDO', 'Post Removido'),
        ('MENCIONADO', 'Usuário Mencionado'),
    ]

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        null=True,
        blank=True
    )
    comment = models.ForeignKey(
        Comment, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        null=True,
        blank=True
    )
    notification_type = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_TYPES
    )
    content = models.TextField()
    created_in = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notificação para {self.user.username} - {self.notification_type}"

    class Meta:
        ordering = ['-created_in']
        verbose_name_plural = "Notificações"