from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

#app_name = "label"

urlpatterns = [
    path('labels/<int:id>', views.labels, name='labels'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

