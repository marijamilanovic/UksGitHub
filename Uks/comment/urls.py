from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
     path('addComment/<int:id>', views.addComment, name='addComment'),
     path('addEmoji/<int:id>/<int:pr_id>', views.addEmoji, name='addEmoji'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)