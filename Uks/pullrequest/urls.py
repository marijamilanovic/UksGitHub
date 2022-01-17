from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

#app_name = "pullrequest"

urlpatterns = [
     path('openedPRs', views.openedPRs, name='openedPRs'),
     path('closedPRs', views.closedPRs, name='closedPRs')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

