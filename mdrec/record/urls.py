from django.urls import path
from . import views


app_name = 'record'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('detail/<int:id>/', views.detail, name='detail'),
]