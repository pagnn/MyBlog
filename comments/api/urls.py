from django.urls import path

from .views import CommentListAPIView,CommentDetailAPIView,CommentCreateAPIView
app_name='comments'
urlpatterns = [
    path('', CommentListAPIView.as_view(),name='thread'),
    path('create/', CommentCreateAPIView.as_view(),name='create'),
    path('<int:pk>/', CommentDetailAPIView.as_view(),name='detail'),
]