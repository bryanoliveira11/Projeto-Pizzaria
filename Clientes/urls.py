from django.urls import path
from . import views

app_name = 'cliente'

urlpatterns = [
    path('', views.Cadastrar.as_view(), name='cadastro'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]
