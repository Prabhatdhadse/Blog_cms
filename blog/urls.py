from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_post, name='create_post'),
    path('edit/<slug:slug>/', views.edit_post, name='edit_post'),
    path('delete/<slug:slug>/', views.delete_post, name='delete_post'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),

]
