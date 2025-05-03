from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . models import Post
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.

@login_required
def index(request):
    user = request.user
    query = Post.objects.filter(author=user)
    paginator = Paginator(query, 4) 
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    
    allPosts = Post.objects.exclude(author=user)
    
    context = {
        'posts': posts,
        'allPosts': allPosts
    }
    return render(request, 'myapp/dashboard.html', context)

@login_required
def createBlog(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Blog created successfully')
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'myapp/createBlog.html', {'form': form})