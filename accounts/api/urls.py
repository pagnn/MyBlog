from django.urls import path

from .views import UserCreateAPIView
app_name='accounts'
urlpatterns = [
    # path('login/', login_view,name='login'),
    # path('logout/', logout_view,name='logout'),
    path('register/', UserCreateAPIView.as_view(),name='register'),
]