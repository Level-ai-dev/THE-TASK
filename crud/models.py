from django.db import models

# Create your models here.
from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=40)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title  # Fixed: was self.name

    class Meta:
        ordering = ["-created_at"]