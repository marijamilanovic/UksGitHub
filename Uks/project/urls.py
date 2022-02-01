from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "project"

urlpatterns = [
    path('all_projects', views.all_projects, name = 'all_projects'),
    path('projects/<int:id>', views.projects, name='projects'),
    path('newProject/<int:id>', views.newProject, name='newProject'),
    path('addProject',views.addProject, name='addProject'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)