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
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

