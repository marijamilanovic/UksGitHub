from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
     path('add_comment/<int:id>', views.add_comment, name='add_comment'),
     path('add_emoji/<int:id>/<int:pr_id>', views.add_emoji, name='add_emoji'),
     path('update_comment/<int:id>/<int:pr_id>', views.update_comment, name='update_comment'),
     path('delete_comment/<int:id>/<int:pr_id>', views.delete_comment, name='delete_comment'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)