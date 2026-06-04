from django.urls import path
from .views import get, post, put, delete  

urlpatterns = [
    path('', get),                      
    path('<int:pk>/', get),             
    path('create/', post),              
    path('<int:pk>/update/', put),     
    path('<int:pk>/delete/', delete),  
]