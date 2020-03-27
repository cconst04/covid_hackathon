from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload_file, name='upload'),
    path('load_postal_codes', views.load_postal_codes, name='load_postal_codes'),
]
