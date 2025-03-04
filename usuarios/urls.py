from django.urls import path
from usuarios import views

# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('criar_usuario', views.criar_usuario, name='criar_usuario'),
    path('login_view', views.login_view, name='login_view'),
    path('ver_usuarios', views.ver_usuario, name='ver_usuarios'),
    path('redefinir_senha', views.redefinir_senha, name='redefinir_senha'),
    path('redirecionar_home', views.redirecionar_home, name='redirecionar_home'),
    path('logout_view', views.logout_view, name='logout_view')
  
]