from django.urls import path
from .views import get, post, put, delete, schedule_post, cancel_scheduled_post, task_status 

urlpatterns = [
    path('', get),                      
    path('<int:pk>/', get),             
    path('create/', post),              
    path('<int:pk>/update/', put),     
    path('<int:pk>/delete/', delete),  
    
    path('posts/schedule/', schedule_post, name='post-schedule'),
    path('posts/<int:pk>/cancel/', cancel_scheduled_post, name='post-cancel'),
    path('posts/<int:pk>/status/',task_status, name='post-status'),
]