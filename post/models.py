

# Create your models here.
from django.db import models
from user.models import user
from django.contrib.auth.models import User

class BlogPost(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE,related_name='posts')
    title = models.CharField(max_length=40)
    slug    = models.SlugField(unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title  # Fixed: was self.name

    class Meta:
        ordering = ["-created_at"]