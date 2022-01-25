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
     path('addComment/<int:id>', comment.views.addComment, name='addComment'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

