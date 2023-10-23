from django.urls import path
from . import views

urlpatterns = [
    path('registerUser/', views.httpRegisterUser, name='registerUser')
]
