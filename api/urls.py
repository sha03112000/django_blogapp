from django.urls import path
from . import views


urlpatterns = [
    path('blogs/',views.BlogListAndCreate.as_view(),name='create_view_blogs'),
    path('blogs/<int:pk>',views.UpdateDeleteBlog.as_view(),name='detail_blogs'),
    path('delete/<int:pk>',views.delete_blog,name='delete_blog'),
]