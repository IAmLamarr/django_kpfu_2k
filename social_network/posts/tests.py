from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from bs4 import BeautifulSoup

from social_network import settings
from .models import Post
import os
from pathlib import Path

# Create your tests here.

class PostTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        image_path = "mock_data/dog_picture.jpeg"
        Post.objects.create(
            title="Test post",
            description="Test post description",
            text="Test post text",
            image=SimpleUploadedFile(
                name='test_post_image.jpg',
                content=open(image_path, 'rb').read(),
                content_type='image/jpeg'
            )
        )
    
    def setUp(self):
        self.c = Client()
        self.test_post = Post.objects.get(title="Test post")
    
    def test_if_simple_routes_is_available(self):
        urls_aliases_to_test = ["posts:create", "posts:create_keyword", "posts:list"]
        for url_alias in urls_aliases_to_test:
            url = reverse(url_alias)
            response = self.c.get(url)
            self.assertEqual(response.status_code, 200)
    
    def test_if_test_post_created(self):
        test_post = Post.objects.get(title="Test post")
        self.assertEqual(test_post.description, "Test post description")
    
    def test_post_delete(self):
        url_alias = "posts:delete"
        url = reverse(url_alias, kwargs={'post_id': self.test_post.id})
        response = self.c.get(url)
        self.assertEqual(response.status_code, 302)
        
        redirect_url_alias = "posts:list"
        redirect_url = reverse(redirect_url_alias)
        self.assertEqual(response.headers.get("Location"), redirect_url)
    
    def test_if_delete_route_work_correct(self):
        url_alias = "posts:delete"
        url = reverse(url_alias, kwargs={'post_id': self.test_post.id})
        self.c.get(url)
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(title=self.test_post.title)
    
    def test_if_detail_works_correct(self):
        url_alias = "posts:detail"
        url = reverse(url_alias, kwargs={'post_id': self.test_post.id})
        response = self.c.get(url)
        bs4 = BeautifulSoup(response.content, "html.parser")
        
        tag_title = bs4.find("title")
        tag_title_text = tag_title.getText().strip()
        self.assertEqual(tag_title_text, f'Пост "{self.test_post.title}"')
        
        card_title_tag = bs4.find(class_="card-title")
        card_tag_title_text = card_title_tag.getText().strip()
        self.assertEqual(card_tag_title_text, self.test_post.title)
        
        card_text_tags = bs4.findAll(class_="card-text")
        self.assertEqual(len(card_text_tags), 2)

        post_desc_tag = card_text_tags[0]
        post_desc_tag_text = post_desc_tag.getText().strip()
        self.assertEqual(post_desc_tag_text, self.test_post.description)
        
        post_text_tag = card_text_tags[1]
        post_text_tag_text = post_text_tag.getText().strip()
        self.assertEqual(post_text_tag_text, self.test_post.text)
        
        post_img_tag = bs4.find("img", class_="card-img-top", src="/media/test_post_image.jpg")
        self.assertIsNotNone(post_img_tag)
    
    def test_if_post_edit_is_available(self):
        urls_aliases_to_test = ["posts:detail", "posts:update"]
        for url_alias in urls_aliases_to_test:
            url = reverse(url_alias, kwargs={'post_id': self.test_post.id})
            response = self.c.get(url)
            self.assertEqual(response.status_code, 200)
        
    @classmethod
    def tearDownClass(cls):
        path = Path(settings.MEDIA_ROOT, "test_post_image.jpg")
        os.remove(path)
