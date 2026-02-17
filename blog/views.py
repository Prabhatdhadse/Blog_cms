from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Post
from django.core.paginator import Paginator


# 🏠 Blog Home Page
def post_list(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(status='published').order_by('-created_at')

    if query:
        posts = posts.filter(title__icontains=query)

    # Pagination
    paginator = Paginator(posts, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'query': query
    })


# 📄 Blog Detail Page
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    return render(request, 'blog/post_detail.html', {'post': post})


# 👤 User Registration
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "blog/register.html", {"form": form})


# 📊 Author Dashboard
@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, "blog/dashboard.html", {"posts": posts})


# 📝 Create Post (Without Admin)
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title' ,'category', 'content', 'status']


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("dashboard")
    else:
        form = PostForm()

    return render(request, "blog/create_post.html", {"form": form})

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = PostForm(instance=post)

    return render(request, "blog/edit_post.html", {"form": form})

@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)

    if request.method == "POST":
        post.delete()
        return redirect("dashboard")

    return render(request, "blog/delete_post.html", {"post": post})

# category ke liye hai
def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published')

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/category_posts.html', {
        'category': category,
        'page_obj': page_obj
    })

