from unicodedata import name
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

#app_name = "commit"

urlpatterns = [
    path('createCommit', views.createCommit, name='newCommit'),
    path('commitList', views.commitList, name='commitList'),
    path('deleteCommit/<int:id>', views.deleteCommit, name='deleteCommit'),
    path('viewFoundCommit/<int:id>', views.viewFoundCommit, name='viewFoundCommit'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

