from django.db import models
from django.utils import timezone
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.urls import reverse
from PIL import Image
from users.models import Town


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    image = models.ImageField(upload_to="post_pics", blank=True, null=True)
    content = models.TextField(blank=False)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    # To redirect the user after they have created a new post
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 400 or img.width > 500:
                default_size = (500, 400)
                img.thumbnail(default_size)
                img.save(self.image.path)

# To Reduce data redundancy
class CommunityRequestPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    content = models.TextField(blank=False)
    date_posted = models.DateTimeField(default=timezone.now)


class Comment(models.Model):
    content = models.TextField(max_length=800, blank=False)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

# Request comments
class RequestComment(models.Model):
    content = models.TextField(max_length=800, blank=False)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(CommunityRequestPost, on_delete=models.CASCADE)


class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')


class PersonalRequest(models.Model):
    thread = models.ForeignKey(ThreadModel, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=500)
    image = models.ImageField(upload_to='request_pics', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)


class Alert(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Town, on_delete=models.CASCADE, default=None)
    content = models.TextField(max_length=1000, blank=False, null=False)
    created_on = models.DateField(default=timezone.now)


class Notification(models.Model):
    MESSAGE = 'message'
    POST = 'post'
    ALERT = 'alert'
    CHOICES = (
        (MESSAGE, 'Message'),
        (POST, 'Post'),
        (ALERT, 'Alert')
    )
    notification_type = models.CharField(max_length=20, choices=CHOICES)
    to_user = models.ForeignKey(User, related_name="notification_to", on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name="notification_from", on_delete=models.CASCADE, null=True)
    #post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="+", blank=True, null=True)
    created_on = models.DateField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    extra_id = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-created_on']