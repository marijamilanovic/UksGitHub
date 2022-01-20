from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

#app_name = "issue"

urlpatterns = [
    path('issues/<int:id>', views.issues, name='issues'),
    path('new-issue/<int:id>', views.new_issue, name='new_issue'),
    path('add-issue', views.add_issue, name='add_issue'),
    path('view-issue/<int:id>', views.view_issue, name='view_issue'),
    path('update-issue/<int:id>', views.update_issue, name='update_issue'),
    path('delete-issue/<int:id>', views.delete_issue, name='delete_issue'),
    path('view-found-issue/<int:id>', views.view_found_issue, name='view_found_issue'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

