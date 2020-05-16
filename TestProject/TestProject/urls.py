from django.conf.urls import include, url
import HttpServer.views
from django.urls import path
"""
TestProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Uncomment next two lines to enable admin:
#from django.contrib import admin
#from django.urls import path

urlpatterns = [
    # Uncomment the next line to enable the admin:
    #path('admin/', admin.site.urls)
    url(r'^$', HttpServer.views.getAllPersonsAndPosts, name='getAllPersonsAndPosts'),
    path('getPersonById', HttpServer.views.getPersonById, name='getPersonById'),
    path('getPostById', HttpServer.views.getPostById, name='getPostById'),
    path('createPerson', HttpServer.views.createPerson, name='createPerson'),
    path('createPost', HttpServer.views.createPost, name='createPost'),
    path('editPerson', HttpServer.views.editPerson, name='editPerson'),
    path('editPost', HttpServer.views.editPost, name='editPost'),
    path('deletePerson', HttpServer.views.deletePerson, name='deletePerson'),
    path('deletePost', HttpServer.views.deletePost, name='deletePost'),
]
