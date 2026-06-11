from django.contrib import admin
from .models import BlogPost
# Register your models here.

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'publish_at']
    list_filter = ['status']
    search_fields = ['title', 'user__username']
    fields = ['user', 'title', 'slug', 'content', 'status', 'publish_at']