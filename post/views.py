from rest_framework import status
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes  
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from celery.result import AsyncResult
from .tasks import publish_scheduled_post

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes




@api_view(['GET'])                           
def get(request, pk=None):
    if pk:
        try:
            post = BlogPost.objects.get(pk=pk)
            serializer = BlogPostSerializer(post)
        except BlogPost.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        posts = BlogPost.objects.all()
        serializer = BlogPostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post(request):
    serializer = BlogPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def put(request, pk):
    try:
        post = BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = BlogPostSerializer(post, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete(request, pk):
    try:
        post = BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    post.delete()
    return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def schedule_post(request):
    publish_at_new = request.data.get('publish_at')

    if not publish_at_new:
        return Response(
            {"error": "publish_at is required. Format: YYYY-MM-DDTHH:MM:SS"},
            status=status.HTTP_400_BAD_REQUEST
        )

    
    scheduled_time = parse_datetime(publish_at_new)
    if not scheduled_time:
        return Response(
            {"error": "Invalid publish_at format. Use YYYY-MM-DDTHH:MM:SS"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if timezone.is_naive(scheduled_time):
        scheduled_time = timezone.make_aware(scheduled_time)


    if scheduled_time <= timezone.now():
        return Response(
            {"error": "publish_at must be a future datetime."},
            status=status.HTTP_400_BAD_REQUEST
        )


    serializer = BlogPostSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    blog_post = serializer.save(
        author=request.user,
        status='scheduled',
        publish_at=scheduled_time,
    )


    result = publish_scheduled_post.apply_async(
        args=[blog_post.id],
        eta=scheduled_time,
    )
    blog_post.task_id = result.id
    blog_post.save(update_fields=['task_id'])

    return Response(
        {
            "message": f"Post scheduled for {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}",
            "post":    BlogPostSerializer(blog_post).data,
            "task_id": result.id,
        },
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_scheduled_post(request, pk):

    try:
        blog_post = BlogPost.objects.get(pk=pk, author=request.user)
    except BlogPost.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    if blog_post.status != 'scheduled':
        return Response(
            {"error": f"Post is '{blog_post.status}', not 'scheduled'. Nothing to cancel."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not blog_post.task_id:
        return Response(
            {"error": "No task ID found for this post."},
            status=status.HTTP_400_BAD_REQUEST
        )

    AsyncResult(blog_post.task_id).revoke()

    blog_post.status     = 'draft'
    blog_post.task_id    = ''
    blog_post.publish_at = None
    blog_post.save(update_fields=['status', 'task_id', 'publish_at'])

    return Response(
        {
            "message": "Scheduled post cancelled and reverted to draft.",
            "post":    BlogPostSerializer(blog_post).data,
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_status(request, pk):
    """
    Check the Celery task state for a scheduled post.
    """
    try:
        blog_post = BlogPost.objects.get(pk=pk, author=request.user)
    except BlogPost.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    if not blog_post.task_id:
        return Response(
            {"error": "No task associated with this post."},
            status=status.HTTP_400_BAD_REQUEST
        )

    result = AsyncResult(blog_post.task_id)

    return Response(
        {
            "post_id":     blog_post.id,
            "post_status": blog_post.status,
            "task_id":     blog_post.task_id,
            "task_state":  result.state,
            "scheduled_for": blog_post.publish_at,
        },
        status=status.HTTP_200_OK
    )