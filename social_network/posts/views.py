from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404
from posts.models import Post, Keyword
from uuid import uuid4, UUID
from django.db.models import Q
from posts.forms import PostForm
from django.forms.models import model_to_dict

def create_keyword(request: HttpRequest):
    if request.method == "POST":
        keyword = Keyword.objects.create(
            name=request.POST.get('name')
        )
        keyword.save()

        return redirect('posts:list')
    return render(request, 'keyword_create.html')

def delete_post(request: HttpRequest, post_id: UUID):
    Post.objects.get(id=post_id).delete()
    return redirect('posts:list')

def posts_list(request: HttpRequest):
    query = request.GET.get('q', None)
    posts_to_return = []
    if query:
        posts_to_return = Post.objects.filter(
            Q(keywords__name__contains=query) |
            Q(description__contains=query) | 
            Q(title__contains=query)
        ).all()
    else:
        posts_to_return = Post.objects.all()

    ctx = {
        "posts": posts_to_return
    }

    return render(request, "list.html", ctx)

def get_post_by_uuid(request: HttpRequest, post_id: UUID):
    post = Post.objects.get(id=post_id)

    ctx = {
        "post": post
    }

    if post is None:
        return Http404()

    return render(request, "detail.html", ctx)

def change_post(request: HttpRequest, post_id: UUID | None = None):
    instance = Post.objects.get(id=post_id) if post_id is not None else None

    if request.method == 'POST':
        if post_id is not None:
            form = PostForm(
                data=request.POST,
                files=request.FILES,
                instance=instance
            )
        else:
            form = PostForm(
                data=request.POST,
                files=request.FILES,
            )
        if form.is_valid():
            data = form.save()
            return redirect('posts:detail', post_id=data.id)

    form = PostForm(
        data=request.POST or None,
        files=request.FILES,
    )

    if instance is not None:
        form = PostForm(
            data=model_to_dict(instance),
            files=request.FILES,
            instance=instance,
        )
    
    ctx = {
        "form": form
    }

    return render(request, 'edit.html', ctx)
    
    # if request.method == "POST":
    #     form = PostForm(request.POST)
    #     form_data = form.data
    #     form_keywords = form_data.getlist('keywords')
    #     db_keywords = Keyword.objects.filter(id__in=form_keywords).all()
    #     image = request.FILES.get('image')
    #     if is_editting:
    #         post=Post.objects.get(id=post_id)
    #         post.title=form_data.get('title')
    #         post.text=form_data.get('text')
    #         post.description=form_data.get('description')
    #         post.image=image
    #         post.keywords.set(db_keywords)
    #     else:
    #         post = Post.objects.create(
    #             title=form_data.get('title'),
    #             text=form_data.get('text'),
    #             description=form_data.get('description'),
    #             # author=form_data.get('author'),
    #             image=image,
    #         )
    #         post.keywords.set(db_keywords)
    #     post.save()
    #     return redirect('posts:detail', post_id=post.id)

    # ctx = {
    #     "form": form
    # }

    # return render(request, 'edit.html', ctx)