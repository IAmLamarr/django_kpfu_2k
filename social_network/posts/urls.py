from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('', views.posts_list, name='list'),
    path('<uuid:post_id>', views.get_post_by_uuid, name='detail'),
    path('create', views.change_post, name='create'),
    path('update/<uuid:post_id>', views.change_post, name='update'),
    path('delete/<uuid:post_id>', views.delete_post, name='delete'),
    path('create_keyword', views.create_keyword, name='create_keyword'),
]