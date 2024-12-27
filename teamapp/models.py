from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator

# Create your models here

class Article(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    posted_at = models.DateTimeField(default=timezone.now)
    published_at = models.DateTimeField(blank=True, null=True)
    like = models.IntegerField(default=0)

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.TextField()
    posted_at = models.DateTimeField(default=timezone.now)
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)


class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    studentid = models.CharField(max_length=10, unique=True,)
    username = models.CharField(max_length=150, unique=True, validators=[username_validator],)
    password = models.CharField(max_length=100,)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["studentid"]

    class Meta:
        db_table = 'custom_user'
    
    def __str__(self):
        return self.username
    
class Profile(models.Model):
    #user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #studentid = models.CharField(max_length=10)
    self_info = models.TextField()
    mbti = models.CharField(max_length=4)
    hobby = models.CharField(max_length=255)
    fav = models.CharField(max_length=255)

    def __str__(self):
        return self.self_info