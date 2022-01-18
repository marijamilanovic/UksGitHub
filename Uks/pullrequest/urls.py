from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

#app_name = "pullrequest"

urlpatterns = [
     path('pullrequests/<int:id>', views.pullrequests, name='pullrequests'),
     path('newPullrequest/<int:id>', views.newPullrequest, name='newPullrequest'),
     path('addPullrequest/', views.addPullrequest, name='addPullrequest'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

