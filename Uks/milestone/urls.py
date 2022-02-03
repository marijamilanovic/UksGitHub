from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

#app_name = "milestone"

urlpatterns = [
    path('newMilestone/<int:id>', views.newMilestone, name='newMilestone'),
    path('milestones/<int:id>', views.milestones, name='milestones'),
    path('allMilestones/', views.allMilestones, name='allMilestones'),
    path('deleteMilestone/<int:id>', views.deleteMilestone, name='deleteMilestone'),
    path('addMilestone/', views.addMilestone, name='addMilestone'),
    path('getMilestoneById/<int:id>', views.getMilestoneById, name='getMilestoneById'),
    path('updateMilestone/<int:id>', views.updateMilestone, name='updateMilestone'),
    path('seeMilestone/<int:id>', views.seeMilestone, name='seeMilestone'),
    path('closeMilestone/<int:id>', views.closeMilestone, name='closeMilestone'),
    path('reopenMilestone/<int:id>', views.reopenMilestone, name='reopenMilestone'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

