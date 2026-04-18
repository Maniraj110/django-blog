from django import forms
from blogs.models import Category, Blog

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-brand'}),
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'short_description', 'blog_body', 'category', 'featured_image', 'status', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-brand',
                'placeholder': 'Enter blog title'
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-brand',
                'placeholder': 'Enter short description',
                'rows': 4
            }),
            'blog_body': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-brand',
                'placeholder': 'Enter blog content',
                'rows': 8
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-brand'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-brand',
                'accept': 'image/*'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-brand'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4'
            }),
        }