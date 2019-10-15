from django.urls import path
from . import views


app_name = 'userprofile'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('confirm/', views.user_confirm, name='confirm'),
    path('center/<int:id>/', views.user_center, name='center'),
    path('create/<int:id>/', views.user_create, name='create'),
    path('logout/', views.user_logout, name='logout'),
]