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
    path('search/', views.search, name = 'search'),
    path('searchedIssues/', views.searchedIssues, name = 'searchedIssues'),
    path('searchedCommits/', views.searchedCommits, name = 'searchedCommits'),
    path('searchedRepositories/', views.searchedRepositories, name = 'searchedRepositories'),
    path('registrate/', views.registrate, name = 'registrate'),
    path('go_to_registration/', views.go_to_registration, name = 'go_to_registration'),
    path('/edit_user/<int:id>', views.edit_user, name = 'edit_user'),
    path('/go_to_edit_user/<int:id>', views.go_to_edit_user, name = 'go_to_edit_user'),
    path('/delete_user/<int:id>', views.delete_user, name = 'delete_user'),
    path('all_users', views.all_users, name = 'all_users'),
    path('searchedUsers', views.searchedUsers, name = 'searchedUsers'),
]

