"""rare_server URL Configuration

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
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import include
<<<<<<< HEAD
from rest_framework import routers
from rare_api.views import register_user, login_user, CommentView, TagView, ReactionView, CategoryView
=======
from rare_api.views import (
    ReactionView,
    CategoryView,
    PostView,
    login_user,
    register_user
)

>>>>>>> main

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'reactions', ReactionView, 'reaction')
router.register(r'categories', CategoryView, 'category')
<<<<<<< HEAD
router.register(r'comments', CommentView, 'comment')
router.register(r'tags', TagView, 'tag')


urlpatterns = [
=======
router.register(r'posts', PostView, 'post')


urlpatterns = [
    path('login', login_user),
    path('register', register_user),
    path('admin/', admin.site.urls),
>>>>>>> main
    path('', include(router.urls))
]
