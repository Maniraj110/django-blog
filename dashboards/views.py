from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from blogs.models import Category, Blog


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
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if category_name:
            category = Category.objects.get(id=category_id)
            category.category_name = category_name
            category.save()
            return redirect('categories')
    category = Category.objects.get(id=category_id)
    return render(request, 'dashboard/category/edit_category.html', {'category': category})

def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect('categories')

def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if category_name:
            Category.objects.create(category_name=category_name)
            return redirect('categories')
    return render(request, 'dashboard/category/add_category.html')

def posts(request):
    posts = Blog.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'dashboard/post/posts.html', context)