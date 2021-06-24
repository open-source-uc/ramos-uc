from django.urls import path
from . import views


app_name = 'comments'
urlpatterns = [
    path('crear', views.create, name='create'),
]
