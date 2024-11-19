from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts_list),
    path('<int:index>', views.get_post_by_index),
    path('<uuid:post_uuid>', views.get_post_by_uuid),
    path('html', views.get_html_page)
]