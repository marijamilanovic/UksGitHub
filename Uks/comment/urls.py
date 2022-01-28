from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
     path('addComment/<int:id>', views.addComment, name='addComment'),
     path('addEmoji/<int:id>/<int:pr_id>', views.addEmoji, name='addEmoji'),
     path('updateComment/<int:id>/<int:pr_id>', views.updateComment, name='updateComment'),
     path('deleteComment/<int:id>/<int:pr_id>', views.deleteComment, name='deleteComment'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)