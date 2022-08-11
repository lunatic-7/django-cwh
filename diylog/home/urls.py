from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('write/', views.write, name='write'),
    path('search/', views.search, name='search'),
    path('login/', views.handleLogin, name='handleLogin'),
    path('logout/', views.handleLogout, name='handleLogout'),
    path('signup/', views.handleSignup, name='handleSignup')
]
