from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

#app_name = "issue"

urlpatterns = [
    path('issues/<int:id>', views.issues, name='issues'),
    path('new-issue/<int:repo_id>', views.new_issue, name='new_issue'),
    path('add-issue', views.add_issue, name='add_issue'),
    path('view-issue/<int:id>', views.view_issue, name='view_issue'),
    path('update-issue/<int:id>', views.update_issue, name='update_issue'),
    path('delete-issue/<int:id>', views.delete_issue, name='delete_issue'),
    path('view-found-issue/<int:id>', views.view_found_issue, name='view_found_issue'),
    path('filter_issues/<int:repo_id>/<str:pk>/', views.filter_issues, name='filter_issues'),
    path('filter_issues/<int:repo_id>/<str:pk>/<int:object_id>', views.filter_issues_for_multiple_objects, name='filter_issues'),
    path('all_issues', views.all_issues, name = 'all_issues'),
    path('load-assignees/<int:repo_id>', views.load_assignees, name='load_assignees'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

