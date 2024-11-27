from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404
from posts.models import Post
import json
import dataclasses
from uuid import uuid4, UUID

"""
    - ID
    - Название
    - Описание
    - Текст
    - Автор
    - Ключевые слова
"""

posts: list[Post] = [
    Post(
        post_id=str(uuid4()),
        title="Пост 1",
        description="Пост про Python",
        text="",
        author="Автор 1",
        keywords=["python", "django", "programming", "dev"],
        image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXqH3qcBehhF3BYcupmrY6mcA3q8KBTKui7g&s",
    ),
    Post(
        post_id=str(uuid4()),
        title="Пост 2",
        description="Пост про HTML",
        text="",
        author="Автор 1",
        keywords=["js", "html", "front", "css", "programming", "dev"],
        image="https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/HTML5_logo_and_wordmark.svg/640px-HTML5_logo_and_wordmark.svg.png",
    ),
    Post(
        post_id=str(uuid4()),
        title="Пост 3",
        description="Пост про devops",
        text="",
        author="Автор 2",
        keywords=["devops", "administration", "linux", "programming"],
        image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQvNOGScTE3oiIaRGMnO0K7j9QVd_vRmu8jOQ&s",
    ),
    Post(
        post_id=str(uuid4()),
        title="Пост 4",
        description="Пост про java",
        text="",
        author="Автор 2",
        keywords=["java", "spring"],
        image="https://upload.wikimedia.org/wikipedia/ru/thumb/3/39/Java_logo.svg/1200px-Java_logo.svg.png",
    ),
    Post(
        post_id=str(uuid4()),
        title="Пост 5",
        description="Пост про c#",
        text="",
        author="Автор 3",
        keywords=["c#", "asp.net"],
        image="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/C_Sharp_Logo_2023.svg/800px-C_Sharp_Logo_2023.svg.png",
    ),
]

def get_all_keywords() -> set[str]:
    all_keywords = set()
    for post in posts:
        all_keywords = all_keywords.union(set(post.keywords))
    return all_keywords

def get_post_index_by_id(post_id: UUID) -> int | None:
    for i in range(len(posts)):
        if posts[i].post_id == str(post_id):
            return i
    return None

def posts_list(request: HttpRequest):
    query = request.GET.get('q', None)
    posts_to_return = []
    if query:
        for post in posts:
            if query in post.keywords or query in post.description or query in post.title:
                 posts_to_return.append(post)
    else:
        posts_to_return = posts

    ctx = {
        "posts": posts_to_return
    }

    return render(request, "list.html", ctx)

def get_post_by_uuid(request: HttpRequest, post_uuid: UUID):
    posts_to_return = None
    for post in posts:
        if post.post_id == str(post_uuid):
            posts_to_return = post

    ctx = {
        "post": posts_to_return
    }

    if posts_to_return is None:
        return Http404()

    return render(request, "detail.html", ctx)

def change_post(request: HttpRequest, post_uuid: UUID | None = None):
    is_editting = post_uuid is not None
    current_post_idx = get_post_index_by_id(post_uuid) if is_editting else None
    if is_editting and current_post_idx is None:
        return Http404()
    
    if request.method == "POST":
        form_data = request.POST
        edit_post_id = str(post_uuid) if is_editting else str(uuid4())
        new_post = Post(
            post_id=edit_post_id,
            title=form_data.get('title'),
            text=form_data.get('text'),
            description=form_data.get('description'),
            author=form_data.get('author'),
            keywords=form_data.getlist('keywords'),
            image=form_data.get('image'),
        )
        if is_editting:
            posts[current_post_idx] = new_post
        else:
            posts.append(new_post)
        return redirect('posts:detail', post_uuid=new_post.post_id)

    ctx = {
        "possible_keywords": list(get_all_keywords()),
        "is_editting": is_editting
    }

    if is_editting:
        ctx = {
            **ctx,
            "post": posts[current_post_idx],
        }

    return render(request, 'edit.html', ctx)