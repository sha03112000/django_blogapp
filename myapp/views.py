from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from .models import Post
from .forms import PostForm


def paginate_queryset(queryset, page_number, per_page=4):
    paginator = Paginator(queryset, per_page)
    try:
        return paginator.page(page_number)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


@login_required
def index(request):
    user_posts = Post.objects.filter(author=request.user)
    other_posts = Post.objects.exclude(author=request.user)

    page_number = request.GET.get("page", 1)
    paginated_posts = paginate_queryset(user_posts, page_number)

    context = {
        'posts': paginated_posts,
        'allPosts': other_posts
    }
    return render(request, 'myapp/dashboard.html', context)


@login_required
def createBlog(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Blog created successfully')
            return redirect('index')
        else:
            messages.error(request, 'Form submission failed. Please check the data.')
    else:
        form = PostForm()

    return render(request, 'myapp/createBlog.html', {'form': form})


@login_required
def updateBlog(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    blog_id = request.POST.get('blogId')
    if not blog_id:
        return JsonResponse({'error': 'Missing blog ID'}, status=400)

    post = get_object_or_404(Post, id=blog_id, author=request.user)

    form = PostForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'Post updated successfully'}, status=200)
    else:
        return JsonResponse({'error': form.errors}, status=400)


@login_required
def deleteBlog(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    post = get_object_or_404(Post, id=pk, author=request.user)
    post.delete()
    return JsonResponse({'message': 'Post deleted successfully'}, status=200)
