"""
Imports
# 3rd party:
"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home, name='home'),
    path("aboutus/", views.AboutUs, name="aboutus"),
    path('trail/', views.PostList.as_view(), name="trail"),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
]