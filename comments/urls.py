from django.urls import path

from .views import comment_thread
app_name='comments'
urlpatterns = [
    path('<int:pk>/', comment_thread,name='thread'),
]