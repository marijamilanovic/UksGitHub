from unicodedata import name
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "insights"

urlpatterns = [
    path('pulse/<int:id>', views.pulse, name='pulse'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

