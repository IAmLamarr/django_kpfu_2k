from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
from posts.models import Post
import json
import dataclasses
from uuid import uuid4, UUID

"""
    - ID
    - Название
    - Описание
    - Автор
    - Ключевые слова
"""

posts: list[Post] = [
    Post(
        post_id=str(uuid4()),
        title="Пост 1",
        description="Пост про Python",
        author="Автор 1",
        keywords=["python", "django", "programming", "dev"],
        image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXqH3qcBehhF3BYcupmrY6mcA3q8KBTKui7g&s",
    ),
    Post(
        post_id=str(uuid4()),
        title="Пост 2",
        description="Пост про HTML",
        author="Автор 1",
        keywords=["js", "html", "front", "css", "programming", "dev"],
        image="https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/HTML5_logo_and_wordmark.svg/640px-HTML5_logo_and_wordmark.svg.png",
    ),
    Post(
        post_id=str(uuid4()),
        title="Пост 3",
        description="Пост про devops",
        author="Автор 2",
        keywords=["devops", "administration", "linux", "programming"],
        image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQvNOGScTE3oiIaRGMnO0K7j9QVd_vRmu8jOQ&s",
    ),
    Post(
        post_id=str(uuid4()),
        title="Пост 4",
        description="Пост про java",
        author="Автор 2",
        keywords=["java", "spring"],
        image="https://upload.wikimedia.org/wikipedia/ru/thumb/3/39/Java_logo.svg/1200px-Java_logo.svg.png",
    ),
    Post(
        post_id=str(uuid4()),
        title="Пост 5",
        description="Пост про c#",
        author="Автор 3",
        keywords=["c#", "asp.net"],
        image="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/C_Sharp_Logo_2023.svg/800px-C_Sharp_Logo_2023.svg.png",
    ),
]

def posts_list(request: HttpRequest):
    query = request.GET.get('q', None)
    posts_to_return = []
    if query:
        for post in posts:
            if query in post.keywords or query in post.description:
                 posts_to_return.append(post)
    else:
        posts_to_return = posts
    json_data = json.dumps([dataclasses.asdict(post) for post in posts_to_return])
    return HttpResponse(json_data, content_type="application/json")

def get_post_by_index(request: HttpRequest, index: int):
    if index > 0 and index < len(posts):
        chosen_post = posts[index - 1]
        json_data = json.dumps(dataclasses.asdict(chosen_post))
        return HttpResponse(json_data, content_type="application/json") 
    error_message = {
        "error": "Not found"
    }
    return HttpResponse(json.dumps(error_message), content_type="application/json", status=404)

def get_post_by_uuid(request: HttpRequest, post_uuid: UUID):
    for post in posts:
        if post.post_id == str(post_uuid):
            json_data = json.dumps(dataclasses.asdict(post))
            return HttpResponse(json_data, content_type="application/json") 
    error_message = {
        "error": "Not found"
    }
    return HttpResponse(json.dumps(error_message), content_type="application/json", status=404)

def get_html_page(request: HttpRequest):
    ctx = {
        "posts": posts
    }
    return render(request, "post_list.html", ctx)
