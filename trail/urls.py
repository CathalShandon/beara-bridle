"""
Imports
# 3rd party:
"""
from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home, name='home'),
    path("aboutus/", views.AboutUs, name="aboutus"),
    path('trail/', views.PostList.as_view(), name="trail"),
    path('create/', views.create_post, name='create_post'),
    path('edit_post/<slug:slug>', views.edit_post, name='post_edit'),
    path('delete_post/<slug:slug>', views.delete_post, name='post_delete'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
]
