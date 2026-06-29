from rest_framework import serializers
from .models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ["id","user","title","slug","content","status","created_at", "published_at"]
        read_only_fields = ["id","user","created_at"]
        
        