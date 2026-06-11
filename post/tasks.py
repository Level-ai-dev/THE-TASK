from .models import BlogPost
from celery import shared_task
from django.utils import timezone

@shared_task
def publish_scheduled_posts():
    due_posts = BlogPost.objects.filter(
        status='scheduled',
        publish_at=timezone.now()
    )
    
    count = due_posts.count()
    
    due_posts.update(
        status = 'published',
        publish_at = timezone.now()
    )
    
    return f"Published {count} post"