"""my_instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path
from Insta.views import (HelloWorld, PostsView, PostDetailView, PostCreateView, 
                        PostUpdateView,PostDeleteView, SignUp, addLike, 
                        UserProfile, EditProfile, addComment,toggleFollow)

urlpatterns = [
    path('helloWorld/', HelloWorld.as_view(), name = 'helloWorld'),
    path('', PostsView.as_view(), name = 'posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post_detail'),
    path('post/new/', PostCreateView.as_view(), name = 'post_create'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name = 'post_update'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name = 'post_delete'),
    path('auth/signup/', SignUp.as_view(), name = 'sign_up'),
    path('like', addLike, name = 'add_like'),
    path('user/<int:pk>', UserProfile.as_view(), name = 'user_profile'),
    path('user/edit/<int:pk>', EditProfile.as_view(), name = 'profile_edit'),
    path('comment', addComment, name = 'add_comment'),
    path('togglefollow', toggleFollow, name='togglefollow'),
]