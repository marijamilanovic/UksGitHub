from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import comment.views

from . import views

#app_name = "pullrequest"

urlpatterns = [
     path('pullrequests/<int:id>', views.pullrequests, name='pullrequests'),
     path('newPullrequest/<int:id>', views.newPullrequest, name='newPullrequest'),
     path('addPullrequest/', views.addPullrequest, name='addPullrequest'),
     path('updatePullrequestPage/<int:id>', views.updatePullrequestPage, name='updatePullrequestPage'),
     path('changeStatusPullrequest/<int:id>', views.changeStatusPullrequest, name='changeStatusPullrequest'),
     path('add_comment/<int:id>', comment.views.add_comment, name='add_comment'),
     path('add_emoji/<int:id>/<int:pr_id>', comment.views.add_emoji, name='add_emoji'),
     path('update_comment/<int:id>/<int:pr_id>', comment.views.update_comment, name='update_comment'),
     path('delete_comment/<int:id>/<int:pr_id>', comment.views.delete_comment, name='delete_comment'),
     path('add_reviewers_on_pull_request/<int:id>', views.add_reviewers_on_pull_request, name='add_reviewers_on_pull_request'),
     path('remove_reviewer_from_pullrequest/<int:pullrequest_id>/<int:reviewer_id>', views.remove_reviewer_from_pullrequest, name='remove_reviewer_from_pullrequest'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

