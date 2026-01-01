from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sale/', views.sale_page, name='sale'),

    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('profile/', views.profile, name='profile'),
]
