from django.urls import path
from . import views
from myapp.utils.custome_reatelimior import rate_limited_view

urlpatterns = [
    path('', rate_limited_view(views.signIn, rate='10/m'), name='signIn'),
    path('signUp/', views.signUp, name='signUp'),
    path('signOut/', views.signOut, name='signOut'),
]