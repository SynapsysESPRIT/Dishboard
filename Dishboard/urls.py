from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from Comment.views import CommentListView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('user/', include('User.urls')),
    path('Recette/', include("Recette.urls")),
    path('Publication/', include("Publication.urls")),
    path('comments/', include('Comment.urls')),  # Include all Comment URLs
    path('comments/list/', CommentListView.as_view(), name='comment_list'),  # Specific view for comment list
    path('Article/', include('Article.urls')),
    path('addinventory', include('inventory.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
