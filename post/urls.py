from django.urls import path
from .views import BlogPostView

urlpatterns = [
    path("posts/", BlogPostView.as_view()),           
    path("posts/<int:pk>/", BlogPostView.as_view()), 
]