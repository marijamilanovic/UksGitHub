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
    path('closeProject/<int:id>', views.closeProject, name='closeProject'),
    path('reopenProject/<int:id>', views.reopenProject, name='reopenProject'),
    path('getProjectById/<int:id>', views.getProjectById, name='getProjectById'),
    path('updateProject/<int:id>', views.updateProject, name='updateProject'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)