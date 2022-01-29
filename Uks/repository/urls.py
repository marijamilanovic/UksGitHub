from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

#app_name = "repository"

urlpatterns = [
    path('<int:id>', views.index, name='repository'),
    path('newRepository', views.newRepository, name='newRepository'),
    path('all_repositories', views.all_repositories, name = 'all_repositories'),
    path('addRepository/', views.addRepository, name = 'addRepository'),
    path('editRepository/', views.editRepository, name = 'editRepository'),
    path('transferToEditRepository/<int:id>', views.transferToEditRepository, name='transferToEditRepository'),
    path('deleteRepository/<int:id>', views.deleteRepository, name='deleteRepository'),
    path('<int:id>/<int:branch_id>', views.repo_branch, name='repo_branch'),
    path('watchRepository/<int:id>', views.watchRepository, name = 'watchRepository'),
    path('watchers/<int:id>', views.watchers, name='watchers'),
    path('starRepository/<int:id>', views.starRepository, name = 'starRepository'),
    path('stargazers/<int:id>', views.stargazers, name='stargazers'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

