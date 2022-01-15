from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

#app_name = "repository"

urlpatterns = [
    path('<int:id>', views.index, name='repository'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

