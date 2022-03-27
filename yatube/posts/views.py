from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import PostForm, CommentForm
from .models import Group, Post, User, Follow


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, settings.NUM_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'posts': posts,
        'title': 'Последние обновления на сайте',
        'text': 'Главная страница',
    }
    return render(request, 'posts/index.html', context)


@login_required(login_url='users:login')
def posts_list(request):
    context = {
        'title': 'Это главная страница проекта Yatube',
        'text': 'Главная страница',
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.groups.all()
    paginator = Paginator(posts, settings.NUM_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author__username=username)
    paginator = Paginator(posts, settings.NUM_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    following = request.user.is_authenticated and Follow.objects.filter(
        user=request.user,
        author=author
    ).exists()
    context = {
        'page_obj': page_obj,
        'author': author,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    posts = Post.objects.get(id=post_id)
    posts_author = Post.objects.filter(author__username=posts.author)
    form = CommentForm(request.POST or None)
    context = {
        'posts_author': posts_author,
        'posts': posts,
        'title': 'Пост ' + posts.text[:30],
        'form': form,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required(login_url='users:login')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(
            request.POST or None,
            files=request.FILES or None,
        )
        if form.is_valid():
            new_text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            image = form.cleaned_data['image']
            Post.objects.create(
                text=new_text,
                group=group,
                author=request.user,
                image=image, )
            return redirect('posts:profile', request.user.username)
        return render(request, 'posts/create_post.html', {'form': form})

    form = PostForm()
    context = {
        'form': form,
        'title': 'Добавить запись',
    }
    return render(request, 'posts/create_post.html', context)


@login_required(login_url='users:login')
def post_edit(request, post_id):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            posts = Post.objects.get(id=post_id)
            posts.text = new_text
            posts.group = group
            posts.save()
            return redirect('posts:post_detail', post_id)
        return render(request, 'posts/create_post.html', {'form': form})
    is_edit = 1
    posts = get_object_or_404(Post, id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=posts
    )
    if request.user == posts.author:
        context = {
            'is_edit': is_edit,
            'form': form,
            'posts': posts,
            'title': 'Редактировать запись',
        }
        return render(request, 'posts/create_post.html', context)
    return redirect('posts:post_detail', post_id)


@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts, settings.NUM_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj,
               'paginator': paginator
               }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author == request.user:
        return redirect(
            'posts:profile',
            username=username
        )
    follower = Follow.objects.filter(
        user=request.user,
        author=author
    ).exists()
    if follower is True:
        return redirect(
            'posts:profile',
            username=username
        )
    Follow.objects.create(user=request.user, author=author)
    return redirect(
        'posts:profile',
        username=username
    )


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    if author == request.user:
        return redirect(
            'posts:profile',
            username=username
        )
    following = get_object_or_404(Follow, user=request.user, author=author)
    following.delete()
    return redirect(
        'posts:profile',
        username=username)
