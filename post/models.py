

# Create your models here.
from django.db import models
from django.conf import settings
from django.utils import timezone

class BlogPost(models.Model):
    status_choices = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='posts')
    title = models.CharField(max_length=200)
    slug    = models.SlugField(unique=True)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=status_choices, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    publish_at = models.DateTimeField(null=True, blank=True)
    published_at_live = models.DateTimeField(null=True, blank=True)
    task_id = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.title 

    class Meta:
        ordering = ["created_at"]