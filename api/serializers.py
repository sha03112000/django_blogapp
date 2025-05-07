from rest_framework import serializers
from myapp.models import Post
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],  # Enforces Django's password policies
        style={'input_type': 'password'}  # For browsable API
    )
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    #hash Password
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class PostSerializer(serializers.ModelSerializer):
    # blog_image_url = serializers.SerializerMethodField()
    blog_image = serializers.ImageField(required=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'blog_image', 'author']
        extra_kwargs = {
            'author': {'read_only': True},
        }
    
    # def get_blog_image_url(self, obj):
    #     request = self.context.get('request')
    #     if obj.blog_image and request:
    #         return request.build_absolute_uri(obj.blog_image.url)
    #     return None
    
    def create(self, validated_data):
        # Handle file upload
        image = validated_data.pop('image', None)
        post = Post.objects.create(**validated_data)
        if image:
            post.image = image
            post.save()
        return post
    