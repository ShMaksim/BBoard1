from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()
    image1 = models.ImageField(upload_to='post_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video1 = models.URLField(blank=True, null=True)
    video2 = models.URLField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    CATEGORY_CHOICES = [
        ('tanks', 'Танки'),
        ('healers', 'Хилы'),
        ('dps', 'ДД'),
        ('traders', 'Торговцы'),
        ('guildmasters', 'Гилдмастеры'),
        ('questgivers', 'Квестгиверы'),
        ('blacksmiths', 'Кузнецы'),
        ('leatherworkers', 'Кожевники'),
        ('alchemists', 'Зельевары'),
        ('spellcasters', 'Мастера заклинаний'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class Response(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='responses')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('new', 'Новый'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонен'),
    ], default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to post: {self.post.title} by {self.author.username}"


class Newsletter(models.Model):
    subject = models.CharField(max_length=255)
    content = models.TextField()
    sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} subscribed to {self.newsletter.subject}"