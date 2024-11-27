from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('', views.posts_list, name='list'),
    path('<uuid:post_uuid>', views.get_post_by_uuid, name='detail'),
    path('create', views.change_post, name='create'),
    path('update/<uuid:post_uuid>', views.change_post, name='update'),
]