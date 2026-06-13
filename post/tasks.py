from celery import shared_task
from django.utils import timezone
from .models import BlogPost


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def publish_scheduled_post(self, post_id):
    try:
        post = BlogPost.objects.get(pk=post_id, status='scheduled')
    except BlogPost.DoesNotExist:
    
        return f'Post {post_id} skipped (not in scheduled state)'

    try:
        post.status     = 'published'
        post.publish_at = timezone.now()  
        post.save(update_fields=['status', 'publish_at'])
        return f'Post "{post.title}" published at {post.publish_at}'

    except Exception as exc:
        raise self.retry(exc=exc)