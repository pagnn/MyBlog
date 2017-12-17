from django.urls import path

from .views import PostListView,PostDetailView,PostCreateView
app_name='posts'
urlpatterns = [
    path('', PostListView.as_view(),name='list'),
    path('create/', PostCreateView.as_view(),name='create'),
    path('<slug:slug>/', PostDetailView.as_view(),name='detail'),
]