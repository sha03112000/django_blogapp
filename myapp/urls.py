from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('createBlog/', views.createBlog, name='createBlog'),
    path('delete/<int:pk>', views.deleteBlog, name='blog'),
    path('update/', views.updateBlog, name='update'),
]

#inproduction
#  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#in devolopment
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)