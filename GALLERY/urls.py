from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', home, name = 'home'),
    path('about',about , name = 'about'),
    path('Error',Error , name = 'Error'),
    path('contact', contact, name = 'contact'),
    # path('blog', blog, name = 'blog'),
    path('collections', collections, name = 'collections'),
    # path('post', post, name = 'post'),
    path('instagram', instagram, name = 'instagram'),
    path('upload_pics', upload_pics, name = 'upload_pics'),
    # path('accounts/', include('allauth.urls')),
    path('albums/<slug:slug>', albums_details, name = 'albums_details'),
]