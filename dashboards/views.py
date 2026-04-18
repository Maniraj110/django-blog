from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

from blogs.models import Category, Blog

from .forms import CategoryForm, BlogForm


@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.all().count()
    published_blogs_count = Blog.objects.filter(status = 'Published').count()
    draft_blogs_count = Blog.objects.filter(status = 'Draft').count()

    context = {
        'category_count' : category_count,
        'published_blogs_count' : published_blogs_count,
        'draft_blogs_count' : draft_blogs_count,
    }

    return render(request, 'dashboard/dashboard.html', context)

def categories(request):
    return render(request, 'dashboard/category/categories.html')

def edit_category(request, category_id):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = Category.objects.get(id=category_id)
            category.category_name = form.cleaned_data['category_name']
            category.save()
            return redirect('categories')
    category = Category.objects.get(id=category_id)
    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'dashboard/category/edit_category.html', context)

def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect('categories')

def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    context = {
        'form': form,
    }
    return render(request, 'dashboard/category/add_category.html', context)

def posts(request):
    posts = Blog.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'dashboard/post/posts.html', context)

def add_post(request):

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():

            post = form.save(commit=False)
            post.author = request.user
            post.save() # Save the post first to get an ID for slug generation

            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id) # post.id will be available after saving the post for the first time
            post.save()


            return redirect('posts')
    form = BlogForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/post/add_post.html', context)

def edit_post(request, post_id):
    post = Blog.objects.get(id=post_id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid(): 
            post = form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()
            return redirect('posts')
        
    form = BlogForm(instance=post)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'dashboard/post/edit_post.html', context)

def delete_post(request, post_id):
    post = Blog.objects.get(id=post_id)
    post.delete()
    return redirect('posts')