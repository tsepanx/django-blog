from django.urls import path

from .views import ProfileView, IndexView, FeedView, get_logged_profile

app_name = 'blog'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('me/', get_logged_profile, name='me'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('feed/', FeedView.as_view(), name='feed'),
]
