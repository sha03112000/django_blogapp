from .models import Post
from django import forms



class PostForm(forms.ModelForm):
    blog_image = forms.ImageField(required=True, error_messages={'required': 'Please upload an image'}, label='Image', widget=forms.FileInput) #error message
    class Meta:
        model = Post
        fields = ['title', 'body', 'blog_image']