from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "branch"

urlpatterns = [
    path('createBranch/<int:id>', views.createBranch, name='createBranch'),
    path('branchList', views.branchList, name='branchList'),
    path('deleteBranch/<int:id>', views.deleteBranch, name='deleteBranch'),
    path('editBranch/<int:id>', views.editBranch, name='editBranch'),
    path('repoBranchList/<int:id>', views.repoBranchList, name='repoBranchList'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

