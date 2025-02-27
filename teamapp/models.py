from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import User

class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    studentid = models.CharField(max_length=10, unique=True)
    username = models.CharField(max_length=150, unique=True, validators=[username_validator])
    password = models.CharField(max_length=100)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["studentid"]

    class Meta:
        db_table = 'custom_user'

    def __str__(self):
        return self.username

class Article(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    posted_at = models.DateTimeField(default=timezone.now)
    published_at = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.TextField()
    posted_at = models.DateTimeField(default=timezone.now)
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')

    def __str__(self):
        return f"{self.user} likes {self.article.title}"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #studentid = models.CharField(max_length=10)
    self_info = models.TextField(verbose_name='自己紹介')
    mbti = models.CharField(verbose_name='MBTI', max_length=4, validators=[RegexValidator(regex='^[IE][NS][TF][JP]$',message='MBTIは有効な4文字の組み合わせである必要があります',),])
    hobby = models.CharField(verbose_name='趣味、特技', max_length=255)
    fav = models.CharField(verbose_name='好きなもの、こと', max_length=255)

    def __str__(self):
        return self.user.username
    
class Notification(models.Model):
    NOTIFY_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFY_TYPES)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.notification_type}"