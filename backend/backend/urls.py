"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from verifier import views
urlpatterns = [
    path('admin/', admin.site.urls),
    #apis for front end and discord bot
    path('api/',include('verifier.urls')),
    #frontend routes
    path('',views.home,name='home'),
    path('verify-link/',views.verify_link_frontend,name='verify_link_frontend'),
    #verifying image
    path('verify-image/',views.verify_image_frontend,name='verify_image_frontend')
    ]
