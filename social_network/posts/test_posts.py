from django.urls import reverse
import pytest
from .models import Post
from bs4 import BeautifulSoup

@pytest.mark.parametrize(
    'url',
    ["posts:create", "posts:create_keyword", "posts:list"]
)
@pytest.mark.django_db
def test_if_simple_routes_is_available(url, client):
    url = reverse(url)
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_if_test_post_created(test_post):
    assert test_post.description == "Test post description"
    assert Post.objects.count() == 1

@pytest.mark.django_db
def test_post_delete(delete_test_post_url, client):
    assert Post.objects.count() == 1
    response = client.get(delete_test_post_url)
    assert Post.objects.count() == 0
    assert response.status_code == 302
    
    redirect_url_alias = "posts:list"
    redirect_url = reverse(redirect_url_alias)
    assert response.headers.get("Location") == redirect_url

@pytest.mark.django_db
def test_if_delete_route_work_correct(client, test_post, delete_test_post_url):
    client.get(delete_test_post_url)
    with pytest.raises(Post.DoesNotExist):
        Post.objects.get(title=test_post.title)

@pytest.mark.django_db
def test_if_detail_works_correct(client, get_test_post_url, test_post):
    url = get_test_post_url("posts:detail")
    response = client.get(url)
    bs4 = BeautifulSoup(response.content, "html.parser")
    
    def get_tag_text(tag):
        return tag.getText().strip()
    
    tag_title = bs4.find("title")
    tag_title_text = get_tag_text(tag_title)
    assert tag_title_text == f'Пост "{test_post.title}"'
    
    card_title_tag = bs4.find(class_="card-title")
    card_tag_title_text = get_tag_text(card_title_tag)
    assert card_tag_title_text == test_post.title
    
    card_text_tags = bs4.findAll(class_="card-text")
    assert len(card_text_tags) == 2

    post_desc_tag = card_text_tags[0]
    post_desc_tag_text = get_tag_text(post_desc_tag)
    assert post_desc_tag_text == test_post.description
    
    post_text_tag = card_text_tags[1]
    post_text_tag_text = get_tag_text(post_text_tag)
    assert post_text_tag_text == test_post.text
    
    post_img_tag = bs4.find("img", class_="card-img-top", src="/media/test_post_image.jpg")
    assert post_img_tag is not None
    
@pytest.mark.django_db
@pytest.mark.parametrize(
    'url_alias',
    ["posts:detail", "posts:update"]
)
def test_if_post_edit_is_available(url_alias, client, get_test_post_url):
    url = get_test_post_url(url_alias)
    response = client.get(url)
    assert response.status_code == 200