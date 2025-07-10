from django.urls import path
from . import  views
urlpatterns = [
    path("verify-link/",views.verify_link,name='verify_link_api'),
    path('verify-image/',views.verify_image,name='verify_image_api')
]
