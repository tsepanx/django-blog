"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('articles/', include('articles.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from users.views import UserViewSet

from rest_framework_simplejwt.views import token_obtain_pair, token_refresh, token_verify

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
# router.register(r'articles', ArticleViewSet)


urlpatterns = [
    path('users/', include('users.urls', namespace='users')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('admin/', admin.site.urls),

    path('rest/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('token/', token_obtain_pair, name='token_obtain_pair'),
    path('token/refresh/', token_refresh, name='token_refresh'),
    path('token/verify/', token_verify, name='token_verify'),
]
