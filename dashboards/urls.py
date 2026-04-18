from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),

    # Category Management
    path('categories/', views.categories, name="categories"),
    path('categories/add/', views.add_category, name="add_category"),
    path('categories/edit/<int:category_id>/', views.edit_category, name="edit_category"),
    path('categories/delete/<int:category_id>/', views.delete_category, name="delete_category"),

    # Post Management

    path('posts/', views.posts, name="posts"),
    path('posts/add/', views.add_post, name="add_post"),
    path('posts/edit/<int:post_id>/', views.edit_post, name="edit_post"),
    path('posts/delete/<int:post_id>/', views.delete_post, name="delete_post"),

    # User Management

    path('users/', views.users, name="users"),
    path('users/add/', views.add_user, name="add_user"),
    path('users/edit/<int:user_id>/', views.edit_user, name="edit_user"),
    path('users/delete/<int:user_id>/', views.delete_user, name="delete_user")
]