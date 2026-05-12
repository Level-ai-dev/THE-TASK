from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer


class BlogPostView(APIView):

    def get(self, request, pk=None):
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


    def post(self, request):
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk):
        try:
            post = BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BlogPostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            post = BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)