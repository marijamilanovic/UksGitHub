from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import comment.views
import milestone.views
import issue.views

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
     path('approve/<int:pullrequest_id>', views.approve, name='approve'),
     path('merge/<int:pullrequest_id>', views.merge, name='merge'),
     path('update_comment/<int:id>/<int:pr_id>', comment.views.update_comment, name='update_comment'),
     path('delete_comment/<int:id>/<int:pr_id>', comment.views.delete_comment, name='delete_comment'),
     path('add_reviewers_on_pull_request/<int:id>', views.add_reviewers_on_pull_request, name='add_reviewers_on_pull_request'),
     path('remove_reviewer_from_pullrequest/<int:pullrequest_id>/<int:reviewer_id>', views.remove_reviewer_from_pullrequest, name='remove_reviewer_from_pullrequest'),
     path('add_assignes_on_pull_request/<int:id>', views.add_assignees_on_pull_request, name='add_assignes_on_pull_request'),
     path('delete_assignees_on_pull_request/<int:id>/<int:assignee_id>', views.delete_assignees_on_pull_request, name='delete_assignees_on_pull_request'),
     path('add_labels_on_pull_request/<int:id>', views.add_labels_on_pull_request, name='add_labels_on_pull_request'),
     path('delete_labels_on_pull_request/<int:id>/<int:label_id>', views.delete_labels_on_pull_request, name='delete_labels_on_pull_request'),
     path('add_milestones_on_pull_request/<int:id>', views.add_milestones_on_pull_request, name='add_milestones_on_pull_request'),
     path('seeMilestone/<int:id>', milestone.views.seeMilestone, name='seeMilestone'),
     path('add_issues_on_pull_request/<int:id>', views.add_issues_on_pull_request, name='add_issues_on_pull_request'),
     path('view_issue/<int:id>', issue.views.view_issue, name='view_issue'),
     path('delete_issues_on_pull_request/<int:id>/<int:pr_id>', views.delete_issues_on_pull_request, name='delete_issues_on_pull_request'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

