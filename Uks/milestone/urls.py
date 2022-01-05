from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

#app_name = "milestone"

urlpatterns = [
    path('newMilestone/', views.newMilestone, name='newMilestone'),
    path('milestones/', views.milestones, name='milestones'),
    path('deleteMilestone/<int:id>', views.deleteMilestone, name='deleteMilestone'),
    path('addMilestone', views.addMilestone, name='addMilestone'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

