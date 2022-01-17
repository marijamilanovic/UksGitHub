from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "branch"

urlpatterns = [
    path('createBranch', views.createBranch, name='newBranch'),
    path('branchList', views.branchList, name='branchList'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

