from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.welcome, name = 'welcome'), 
    path('login/', views.loginUser, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('/', views.home, name = 'home'),
    path('/profile/', views.profile, name = 'profile'),
    path('registrate/', views.registrate, name = 'registrate'),
    path('go_to_registration/', views.go_to_registration, name = 'go_to_registration')
]

