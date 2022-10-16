from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Group, User
from .forms import PostForm
from django.shortcuts import redirect
from django.core.paginator import Paginator


text_output: int = 10


def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.all()
    paginator = Paginator(post_list, text_output)
    page_number = request.GET.get('page')
    if(not page_number):
        page_number = 1
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'post_list': post_list,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts_group.all()[:text_output]
    paginator = Paginator(posts, text_output)
    page_number = request.GET.get('page')
    if(not page_number):
        page_number = 1
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': group,
        'posts': posts
    }
    return render(request, template, context)


def profile(request, username):
    page_number = request.GET.get('page')
    profile = get_object_or_404(User, username=username)
    post_list = profile.posts_author.all()
    post_count = post_list.count
    paginator = Paginator(post_list, text_output)
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': profile,
        'page_obj': page_obj,
        'paginator': paginator,
        'post_count': post_count
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/post_create.html'
    author = get_object_or_404(User, pk=request.user.id)
    form = PostForm(request.POST or None, initial={'author': author.id})
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(
            'posts:profile', request.user
        )
    return render(request, template, {'form': form})


@login_required
def post_edit(request, post_id):
    template = 'posts/post_create.html'
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post)

    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    return render(request, template,
                  {'form': form, 'is_edit': True, 'post': post}
                  )