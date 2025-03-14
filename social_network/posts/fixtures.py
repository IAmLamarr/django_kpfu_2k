from django.urls import reverse
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Post
from social_network import settings
from pathlib import Path
import os

@pytest.fixture
def test_post():
    image_path = "mock_data/dog_picture.jpeg"
    new_image_name = "test_post_image.jpg"
    
    post = Post.objects.create(
        title="Test post",
        description="Test post description",
        text="Test post text",
        image=SimpleUploadedFile(
            name=new_image_name,
            content=open(image_path, 'rb').read(),
            content_type='image/jpeg'
        )
    )
    
    yield post
    
    path = Path(settings.MEDIA_ROOT, new_image_name)
    os.remove(path)

@pytest.fixture
def delete_test_post_url(get_test_post_url):
    url_alias = "posts:delete"
    return get_test_post_url(url_alias)

@pytest.fixture
def get_test_post_url(test_post):
    def inner(url_alias):
        return reverse(url_alias, kwargs={'post_id': test_post.id})
    return inner