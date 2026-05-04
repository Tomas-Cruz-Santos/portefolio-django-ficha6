from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('magic-link/', views.magic_link_request, name='magic_link_request'),
    path('magic-link/<str:token>/', views.magic_link_verify, name='magic_link_verify'),
]