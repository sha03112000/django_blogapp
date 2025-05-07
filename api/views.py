from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView

from api.permissions import StaticTokenPermission
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import PostSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from myapp.models import Post
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.

class PostPagination(PageNumberPagination):
    page_size = 3
    page_query_param = "page_size"
    max_page_size = 100
    
class CustomeObtainSerializer(TokenObtainPairView):
    permission_classes = [StaticTokenPermission]
    serializer_class = TokenObtainPairSerializer
    
class CreateUser(APIView):
    permission_classes = [StaticTokenPermission]
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response({
                "user": serializer.data,
                "message": "User created successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BlogListAndCreate(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, StaticTokenPermission]
    pagination_class = PostPagination
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request, format=None):
        try:
            user = self.request.user
            paginator = self.pagination_class()
            
            user_posts = Post.objects.filter(author=user).order_by('-created_at')
            paginated_user_posts = paginator.paginate_queryset(user_posts, request, view=self)
            user_posts_serializer = self.serializer_class(paginated_user_posts, many=True, context={'request': request})
            pagination_data = paginator.get_paginated_response(user_posts_serializer.data).data
            
            all_posts = Post.objects.exclude(author=user)
            all_posts_serializer = self.serializer_class(all_posts, many=True, context={'request': request})
            
            # return paginator.get_paginated_response({
            #     'success': True,
            #     'message': 'Posts fetched successfully',
            #     'user_posts': pagination_data,
            #     'all_posts': all_posts_serializer.data
            # })
            
            return Response({
                'success': True,
                'message': 'Posts fetched successfully',
                'user_posts': pagination_data,
                'all_posts': all_posts_serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
    def post(self, request, format=None ):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                post = serializer.save(author=request.user)
                
                if post:
                    return Response({
                        'success': True,
                        'message': 'Post created successfully',
                        'post': serializer.data
                    }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class UpdateDeleteBlog(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, StaticTokenPermission]
    parser_classes = (MultiPartParser, FormParser)
    
    def put(self, request, pk, format=None):
        try:
            post = Post.objects.get(id=pk)
            serializer = self.serializer_class(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'message': 'Post updated successfully',
                    'post': serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Post not found',
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def delete(self, request, pk, format=None):
        try:
            post = Post.objects.get(id=pk, author=request.user)
            post.delete()  # Deletes the post and its associated image if it exists
            return Response({
                'success': True,
                'message': 'Post deleted successfully',
            }, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Invalid post ID or you do not have permission to delete this post',
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
def list_blogs():
    pass

def detail_blogs():
    pass

def delete_blog():
    pass